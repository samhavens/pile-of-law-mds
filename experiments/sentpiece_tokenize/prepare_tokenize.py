"""
convert to sentences on newlines text file for sentencepiece

only have lengths in gpt2 tokens, estimate to get chars

#################### Sequence Length distribution ####################
p50: 2252 * 3.5 = 7882 
p75: 5378 * 3.5 = 18_823
p99: 77989 * 3.5 = 273_000

7406292 total samples
mean sample length: 7019 tokens *3.5 = 24_566
51987222437 tokens

run with 
composer prepare_tokenize.py ../mds-pol

or

torchrun \
    --rdzv_backend=c10d \
    --rdzv_endpoint=localhost:0 \
    --nnodes=1 \
    --nproc_per_node=1 \
    prepare_tokenize.py ../mds-pol
"""

import random
import shutil
from typing import List, Optional
from multiprocessing import Pool

import spacy
import tqdm
from omegaconf import OmegaConf
import streaming as ms


p50 = 7882 
p75 = 18_823
p99 = 273_000


def get_sents(sents: List[str], k:int) -> List[str]:
    if len(sents) < k:
        return sents
    return random.sample(sents, k)


def num_sents_from_len(doc: str) -> int:
    if len(doc) < p50:
        return 1
    elif len(doc) > p75:
        return 4
    else:
        return 2


class SentencesPileOfLaw(ms.StreamingDataset):
    def __init__(self,
                 nlp,
                 local: str,
                 remote: Optional[str] = None,
                 split: Optional[str] = None,
                 shuffle: bool = False,
                 predownload: Optional[int] = 100_000,
                 keep_zip: Optional[bool] = None,
                 download_retry: int = 2,
                 download_timeout: float = 60,
                 validate_hash: Optional[str] = None,
                 shuffle_seed: Optional[int] = None,
                 num_canonical_nodes: Optional[int] = None,
                 batch_size: Optional[int] = None) -> None:

        super().__init__(local, remote, split, shuffle, predownload, keep_zip, download_retry,
                         download_timeout, validate_hash, shuffle_seed, num_canonical_nodes,
                         batch_size)
        self.nlp = nlp

    def __getitem__(self, idx: int) -> List[str]:
        """Get sample by global index, blocking to load its shard if missing.
        Args:
            idx (int): Sample index.
        Returns:
            Any: Sample data.
        """
        text_sample = super().__getitem__(idx)
        text = text_sample['text']
        if len(text) > p75:
            # sorry, for speed
            text = text[:p75]
        return text


def process_chunk(chunk, file_index):
    with open(f'pol_sentences_{file_index}.txt', 'w') as f:
        for sample in chunk:
            for sentence in sample:
                f.write(sentence + "\n")


def chunkify(iterable, chunk_size):
    iterator = iter(iterable)
    while True:
        chunk = []
        try:
            for _ in range(chunk_size):
                chunk.append(next(iterator))
            yield chunk
        except StopIteration:
            if chunk:
                yield chunk
            break


def get_ds_chunks(nlp, PROCS):
    remote = '../mds-pol'
    local = '../mds-pol'
    cfg = {
        'name': 'pile_of_law',
        'dataset': {
            'remote': remote,
            'local': local,
            'split': 'train',
            'shuffle': True,
            'prefetch': 1000,
        },
        'drop_last': False,
        'num_workers': 1,
        'pin_memory': True,
        'prefetch_factor': 2,
        'persistent_workers': True,
        'timeout': 1200,
    }
    cfg = OmegaConf.create(cfg)
    # check this
    device_batch_size = 1
    print(f'Reading {cfg.dataset.split} split from {remote} -> {local}')

    ds_train = SentencesPileOfLaw(
        nlp,
        split='train',
        local=cfg.dataset.local,
        remote=cfg.dataset.remote,
        shuffle=cfg.dataset.shuffle,
        batch_size=device_batch_size,
    )

    chunks = chunkify(ds_train, chunk_size=7406292//PROCS)
    return chunks


def main():
    try:
        nlp = spacy.load('en_core_web_sm', exclude=["ner"])
    except OSError:
        # need model for sentence segmenting
        print("MISSING SENTENCE SEGMENTING MODEL\n\nrun:\npython -m spacy download en_core_web_sm\n\n")
        exit()

    # how much parallelism
    PROCS = 48

    print("chunking")
    chunks = get_ds_chunks(nlp, PROCS)

    for i, chunk in enumerate(chunks):
        print(f"processing chunk {i}")
        docs = nlp.pipe(chunk, n_process=PROCS)
        chunk_sents = []
        for doc in docs:
            k = num_sents_from_len(doc.text)
            sents = [s.text for s in doc.sents if s.text.strip() != '']
            sents = [s.replace('\n', '\\n') for s in sents]  # there are so many newlines, preserve?
            # need to do that bc output format is newline separated strings
            sents = get_sents(sents=sents, k=k)
            chunk_sents += sents
        with open(f'pol_sentences_{i}.txt', 'w') as f:
            for sample in chunk_sents:
                for sentence in sample:
                    f.write(sentence + "\n")

    # with Pool(PROCS) as p:
    #     for _ in tqdm.tqdm(p.imap_unordered(process_chunk, chunks), total=PROCS):
    #         pass

    # Merge the files
    with open('pol_sentences.txt', 'w') as outfile:
        for i in range(PROCS):
            with open(f'pol_sentences_{i}.txt') as infile:
                shutil.copyfileobj(infile, outfile)


if __name__ == "__main__":
    main()