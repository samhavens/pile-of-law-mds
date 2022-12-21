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