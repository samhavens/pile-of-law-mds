# Copyright 2022 MosaicML Benchmarks authors
# SPDX-License-Identifier: Apache-2.0

"""Build a StreamingC4 dataset and dataloader for testing the conversion worked."""

import os
import sys
from itertools import islice
from typing import Any, Dict, Iterator, Optional

import numpy as np
import streaming as ms
import transformers
from omegaconf import DictConfig
from omegaconf import OmegaConf as om
from torch.utils.data import DataLoader


class SimpleStreamingPileOfLaw(ms.StreamingDataset):
    """Implementation of the the Pile using StreamingDataset.
    Args:
        tokenizer_name (str): The name of the HuggingFace tokenizer to use to tokenize samples.
        max_seq_len (int): The max sequence length of each token sample.
        local (str): Local dataset directory where shards are cached by split.
        remote (str, optional): Download shards from this remote path or directory. If None, this
            rank and worker's partition of the dataset must all exist locally. Defaults to
            ``None``.
        split (str, optional): Which dataset split to use, if any. Defaults to ``None``.
        shuffle (bool): Whether to iterate over the samples in randomized order. Defaults to
            ``False``.
        predownload (int, optional): Target number of samples ahead to download the shards of while
            iterating. Defaults to ``100_000``.
        keep_zip (bool, optional): Whether to keep or delete the compressed file when
            decompressing downloaded shards. If set to None, keep iff remote is local. Defaults to
            ``None``.
        download_retry (int): Number of download re-attempts before giving up. Defaults to ``2``.
        download_timeout (float): Number of seconds to wait for a shard to download before raising
            an exception. Defaults to ``60``.
        validate_hash (str, optional): Optional hash or checksum algorithm to use to validate
            shards. Defaults to ``None``.
        shuffle_seed (int, optional): Seed for shuffling, or ``None`` for random seed. Defaults to
            ``None``.
        num_canonical_nodes (int, optional): Canonical number of nodes for shuffling with resumption.
            Defaults to ``None``, which is interpreted as the number of nodes of the initial run.
        batch_size (int, optional): Batch size of its DataLoader, which affects how the dataset is
            partitioned over the workers. Defaults to ``None``.
    """

    def __init__(self,
                 tokenizer_name: str,
                 max_seq_len: int,
                 local: str,
                 remote: Optional[str] = None,
                 split: Optional[str] = None,
                 shuffle: bool = False,
                 predownload: Optional[int] = 100_000,
                 keep_zip: Optional[bool] = True,
                 download_retry: int = 2,
                 download_timeout: float = 60,
                 validate_hash: Optional[str] = None,
                 shuffle_seed: Optional[int] = None,
                 num_canonical_nodes: Optional[int] = None,
                 batch_size: Optional[int] = None) -> None:

        super().__init__(local, remote, split, shuffle, predownload, keep_zip, download_retry,
                         download_timeout, validate_hash, shuffle_seed, num_canonical_nodes,
                         batch_size)
        self.tokenizer_name = tokenizer_name
        self.max_seq_len = max_seq_len

        # Build tokenizer
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(self.tokenizer_name)
        if self.tokenizer.pad_token is None:
            # Some tokenizers (e.g. GPT2 tokenizer) have no padding token which causes bugs
            self.tokenizer.pad_token = self.tokenizer.eos_token

    def _tokenize(self, text_sample: Dict[str, Any]):
        """Apply the tokenizer to a sample.
        Args:
            text_sample (Dict[str, Any]): Sample to tokenize.
        """
        return self.tokenizer(text_sample['text'],
                              truncation=False,
                              padding=False)

    def __getitem__(self, idx: int) -> Any:
        """Get sample by global index, blocking to load its shard if missing.
        Args:
            idx (int): Sample index.
        Returns:
            Any: Sample data.
        """
        text_sample = super().__getitem__(idx)
        token_sample = self._tokenize(text_sample)
        # Skip any token grouping
        return token_sample


class StreamingPileOfLaw(ms.StreamingDataset):
    """Implementation of the C4 dataset using MosaicML's streaming Dataset V2.
    Args:
        remote (str): Remote directory (S3 or local filesystem) where dataset
            is stored.
        local (str): Local filesystem directory where dataset is cached
            during operation.
        split (str): The dataset split to use, either 'train' or 'validation'.
        shuffle (bool): Whether to shuffle the samples in this dataset.
        tokenizer_name (str): The name of the HuggingFace tokenizer to use to
            tokenize samples.
        max_seq_len (int): The max sequence length of each sample.
        group_method (str): How to group text samples into token samples.
            Supports 'truncate' or 'concat'.
        batch_size (Optional[int]): Hint batch_size that will be used on
            each device's DataLoader. Default: ``None``.
    """

    def __init__(self,
                 remote: str,
                 local: str,
                 split: str,
                 shuffle: bool,
                 tokenizer_name: str,
                 max_seq_len: int,
                 group_method: str = 'truncate',
                 batch_size: Optional[int] = None):
        # Validation
        if split not in ['train', 'validation']:
            raise ValueError(
                f"split='{split}' must be one of ['train', 'validation'].")
        if group_method not in ['truncate', 'concat']:
            raise ValueError(
                f"group_method='{group_method}' must be one of ['truncate', 'concat']."
            )

        # Build Dataset
        super().__init__(remote=remote,
                         local=local,
                         split=split,
                         shuffle=shuffle,
                         keep_zip=False,
                         batch_size=batch_size)
        self.tokenizer_name = tokenizer_name
        self.max_seq_len = max_seq_len
        self.group_method = group_method

        # Build tokenizer
        os.environ['TRANSFORMERS_NO_ADVISORY_WARNINGS'] = '1'
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(
            self.tokenizer_name)
        if self.tokenizer.pad_token is None:
            # Some tokenizers (e.g. GPT2 tokenizer) have no padding token which causes bugs
            self.tokenizer.pad_token = self.tokenizer.eos_token
        # suppress warnings when using group_method='concat' and no truncation
        self.tokenizer.model_max_length = int(1e30)

    # How to tokenize a text sample to a token sample
    def _tokenize(self, text_sample):
        if self.group_method == 'truncate':
            truncation = True
            padding = 'max_length'
            max_length = self.max_seq_len
        elif self.group_method == 'concat':
            truncation = False
            padding = False
            max_length = None
        else:
            raise ValueError(f"Got unknown group_method='{self.group_method}'.")
        return self.tokenizer(text_sample['text'],
                              truncation=truncation,
                              padding=padding,
                              max_length=max_length)

    # How to process a sample
    def __getitem__(self, idx: int) -> Dict[str, Any]:
        text_sample = super().__getitem__(idx)
        token_sample = self._tokenize(text_sample)
        return token_sample

    # Define iterable over samples
    # Usually this can be left alone and inherited directly from super()
    # class StreamingDataset, but concatenating samples is custom behavior.
    # If group_method=='truncate', we simply return the token sample.
    # If group_method=='concat', then we keep fetching token samples until we
    # fill up max_seq_len.
    def __iter__(self) -> Iterator[Any]:
        if self.group_method == 'truncate':
            iterator = super().__iter__()
            yield from iterator

        elif self.group_method == 'concat':
            buffer = {}
            while True:
                iterator = super().__iter__()
                for sample in iterator:

                    for k, v in sample.items():
                        buffer[k] = buffer.get(k, []) + v
                    while len(buffer['input_ids']) >= self.max_seq_len:
                        concat_sample = {}
                        for k, v in buffer.items():
                            concat_sample[k] = v[:self.max_seq_len]
                            buffer[k] = v[self.max_seq_len:]
                        yield concat_sample
        else:
            raise ValueError(f"Got unknown group_method='{self.group_method}'.")

    # Define length
    # Usually this can be left alone and inherited directly from super() class
    # Dataset, but concatenating samples is custom behavior.
    # If group_method=='truncate', we simply return the # samples.
    # If group_method=='concat', we repeat forever, and have no defined length.
    def __len__(self) -> Optional[int]:
        if self.group_method in ['truncate']:
            return super().__len__()
        elif self.group_method == 'concat':
            return None
        else:
            raise ValueError(f"Got unknown group_method='{self.group_method}'.")


def build_pile_of_law_dataloader(cfg: DictConfig, device_batch_size: int):
    assert cfg.name == 'pile_of_law', f'Tried to build pile_of_law dataloader with cfg.name={cfg.name}'
    dataset = SimpleStreamingPileOfLaw(split=cfg.dataset.split,
                                 remote=cfg.dataset.remote,
                                 local=cfg.dataset.local,
                                 shuffle=cfg.dataset.shuffle,
                                 tokenizer_name=cfg.dataset.tokenizer_name,
                                 max_seq_len=cfg.dataset.max_seq_len,
                                 batch_size=device_batch_size)

    collate_fn = transformers.DataCollatorForLanguageModeling(
        tokenizer=dataset.tokenizer, mlm=False)

    return DataLoader(
        dataset,
        collate_fn=collate_fn,
        batch_size=device_batch_size,
        drop_last=cfg.drop_last,
        num_workers=cfg.num_workers,
        pin_memory=cfg.pin_memory,
        prefetch_factor=cfg.prefetch_factor,
        persistent_workers=cfg.persistent_workers,
        timeout=cfg.timeout,
    )


# Helpful to test if your dataloader is working locally
# Run `python test_load.py [remote] [local, optional]` and verify that batches are printed out
if __name__ == '__main__':
    remote = sys.argv[1]
    if len(sys.argv) > 2:
        local = sys.argv[2]
    else:
        local = remote

    cfg = {
        'name': 'pile_of_law',
        'dataset': {
            'remote': remote,
            'local': local,
            'split': 'train',
            'shuffle': True,
            'prefetch': 1000,
            'tokenizer_name': 'gpt2',
            'max_seq_len': 256000,  # don't want to truncate for test, these are LONG
            'group_method': 'none' # for length test
        },
        'drop_last': False,
        'num_workers': 8,
        'pin_memory': True,
        'prefetch_factor': 2,
        'persistent_workers': True,
        'timeout': 1200,
    }
    cfg = om.create(cfg)
    # set device batch size to 1, otherwise there will be padding!
    device_batch_size = 1

    print(f'Reading {cfg.dataset.split} split from {remote} -> {local}')

    loader = build_pile_of_law_dataloader(cfg, device_batch_size)
    tokenizer = loader.dataset.tokenizer  # type: ignore
    # for batch_ix, batch in enumerate(islice(loader, 5)):
    #     print('\n')
    #     print('#' * 20, f'Batch {batch_ix}', '#' * 20)
    #     for k, v in batch.items():
    #         print(k, v.shape, v.dtype)
    #     for sample_ix, token_sample in enumerate(batch['input_ids']):
    #         if sample_ix == 0:
    #             print('-' * 20, f' Sample {sample_ix} ', '-' * 20)
    #             print(tokenizer.decode(token_sample))

    # get average token's per sample
    token_lengths = []
    print('\n')
    for batch in islice(loader, 150_000):
        for sample in batch['input_ids']:
            token_lengths.append(len(sample))
    mean = np.mean(token_lengths)
    print('#' * 20, "Sequence Length distribution", '#' * 20)
    print('#' * 20)
    print(f"mean sample length: {mean}")
    for percentile in [1, 5, 10, 30, 50, 75, 80, 90, 95, 99]:
        print(f"p{percentile}: {np.percentile(token_lengths, percentile)}")
    print('#' * 20)

    print(f"{loader.dataset.index.total_samples} total samples")
    print(f"mean sample length: {round(mean)} tokens")
    print(f"{round(loader.dataset.index.total_samples * mean)} tokens")
    exit() # need to run with torchrun and doesn't know to die
