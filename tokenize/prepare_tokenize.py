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
from typing import List

import spacy

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


