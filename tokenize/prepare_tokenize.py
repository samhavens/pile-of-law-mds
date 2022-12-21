"""
convert to sentences on newlines text file for sentencepiece

only have lengths in gpt2 tokens, estimate to get chars

#################### Sequence Length distribution ####################
p50: 2252 * 3.5 = 7882 
p75: 5378 * 3.5 = 18_823

7406292 total samples
mean sample length: 7019 tokens *3.5 = 24_566
51987222437 tokens

run with 
torchrun
    --rdzv_backend=c10d
    --rdzv_endpoint=localhost:0
    --nnodes=1
    --nproc_per_node=1
    prepare_tokenize.py ../mds-pol
"""

import random
from typing import Any, List, Optional

import spacy
import streaming as ms

try:
    spacy.load('en_core_web_sm')
except OSError:
    # need model for sentence segmenting
    print("run python -m spacy download en_core_web_sm")
    exit()


p50 = 7882 
p75 = 18_823


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
        doc = self.nlp(text_sample['text'])
        k = num_sents_from_len(doc.text)
        sents = [s.text for s in doc.sents if s.text.strip() != '']
        sents = get_sents(sents=sents, k=k)
        return sents


def main():
    cfg = {
        'name': 'pile_of_law',
        'dataset': {
            'remote': '../mds-pol',
            'local': '../mds-pol',
            'split': 'train',
            'shuffle': True,
            'prefetch': 1000,
        },
        'drop_last': False,
        'num_workers': 8,
        'pin_memory': True,
        'prefetch_factor': 2,
        'persistent_workers': True,
        'timeout': 1200,
    }
    cfg = om.create(cfg)