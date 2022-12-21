# Pile of Law MDS

This code downloads [The Pile of Law](https://huggingface.co/datasets/pile-of-law/pile-of-law) from the HF Hub and converts it to MDS format.

## Process

1. `hf_download.py` to download the data locally, using the HuggingFace `datasets` wrapper
2. `hf_convert.py` to convert the data to MDS format
3. `test_load.py` to make sure that the resulting MDS file loads, as well as get estimated statistics of the tokenized dataset.
4. Then the MDS folder, `mds-pol` by default, needs to be uploaded to S3. `upload.sh` will do this if you use the default folder names, and want to upload to the only bucket I have access to.

## Alternate Path

My first attempt at doing this was to use `experiments/download_pol.py` for step 1 and `experiments/convert.py` for step 2. These do not use the HuggingFace dataset library, and download the data directly, and convert it straight from the `jsonl.xz` files. This process does not work, and I am not sure why, but I think figuring it out would help for onboarding customers onto Streaming, since I tried to follow the example closely.
