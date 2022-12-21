# based on https://huggingface.co/course/chapter6/2?fw=pt
# sequences process at ~1000samples / sec, total of 1M => ~20min to preprocess at 1M samples
# followed by unknown tokenization time

# if you try to process the whole dataset, it exits with "killed"
# (still plenty of memory according to htop, 64 cores 500GB ram)
# during preprocessing
# using 1M samples, it completes pre-processing, tokenizing, and Count Pairs, then exits with killed

import datasets
from transformers import AutoTokenizer


def get_training_corpus(dataset, total_samples):
    for start_idx in range(0, total_samples, 1000):
        samples = dataset[start_idx : start_idx + 1000]
        yield samples["text"]


def main():
    VOCAB_SIZE = 52_000 # 65_563 # 52_000 for gpt5, 256_000 for PaLM
    TOKENIZER_NAME = "pile-of-law-tokenizer"

    ds = datasets.load_dataset("pile-of-law/pile-of-law", "all", cache_dir="hf_pol")
    dataset = ds['train'].shuffle(seed=42)

    # total_samples = len(dataset)
    # total_samples = 1_000_000
    total_samples = 500_000

    training_corpus = get_training_corpus(dataset, total_samples)

    old_tokenizer = AutoTokenizer.from_pretrained("gpt2")
    tokenizer = old_tokenizer.train_new_from_iterator(training_corpus, VOCAB_SIZE, length=total_samples)
    # save
    tokenizer.save_pretrained(TOKENIZER_NAME)

    # upload
    # you must have run hunggingface_cli login prior to this
    tokenizer.push_to_hub(TOKENIZER_NAME, use_auth_token=True)


if __name__ == "__main__":
    main()