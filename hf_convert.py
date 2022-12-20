# Copyright 2022 MosaicML Streaming authors
# SPDX-License-Identifier: Apache-2.0

"""Convert the Pile of Law dataset to streaming format. DOESN'T WORK YET.

The idea is to take in the HF version of the dataset and convert it, in case something is going wrong upstream.

Based on the Mosiac Streaming example of converting The Pile

    Instructions:
Download the Pile of Law dataset (cf https://huggingface.co/datasets/pile-of-law/pile-of-law/tree/main/data)
or by using HuggingFace datasets.
That will result in this directory structure:
    TODO fill in this directory structure
    data/
        train.*.jsonl.xz
        validation.*.jsonl.xz

Note that this is slightly different than the Pile's structure. There are multiple validation files,
and no test file

You then run this script specifying --in_root (the above dir), --out_root (the dir to create),
and any other flags as appropriate, e.g.

python convert.py --out_root $(pwd)/mds-pol
"""

import json
import lzma
import os
from argparse import ArgumentParser, Namespace
from collections import Counter
from glob import glob
from multiprocessing import Pool
from typing import Dict, Iterator, List, Tuple
import datasets

from streaming.base import MDSWriter
from streaming.base.util import get_list_arg


def parse_args() -> Namespace:
    """Parse command-line arguments.
    Args:
        Namespace: command-line arguments.
    """
    args = ArgumentParser()
    args.add_argument(
        '--out_root',
        type=str,
        required=True,
        help='Directory path to store the output dataset',
    )
    args.add_argument(
        '--compression',
        type=str,
        default='zstd:16',
        help='Compression algorithm to use. Empirically, Zstandard has the best performance in ' +
        'our benchmarks. Tune the compression level (from 1 to 22) to trade off time for ' +
        'quality. Default: zstd:16',
    )
    args.add_argument(
        '--hashes',
        type=str,
        default='sha1,xxh64',
        help='Hashing algorithms to apply to shard files. Default: sha1,xxh64',
    )
    args.add_argument(
        '--size_limit',
        type=int,
        default=1 << 27,
        help='Shard size limit, after which point to start a new shard. Default: 1 << 27',
    )
    args.add_argument(
        '--num_proc',
        type=int,
        default=None,
        help='Number of processes to use, defaults to all available cores',
    )
    args.add_argument(
        '--validation_only',
        action='store_true',
        help='If set, only process the validation split',
    )
    # Source dataset has errors and currently val is broken
    args.add_argument(
        '--train_only',
        action='store_true',
        help='If set, only process the train split',
    )
    return args.parse_args()


def each_task(in_root: str, out_root: str, compression: str, hashes: List[str], size_limit: int,
              in_files: List[str]) -> Iterator[Tuple[str, str, str, List[str], int]]:
    """Get the arg tuple corresponding to each JSONL input file to convert to streaming.
    Args:
        in_root (str): Root directory of input JSONL files.
        out_root (str): Root directory of output MDS files.
        compression (str): Which compression algorithm to use, or empty if none.
        hashes (List[str]): Hashing algorithms to apply to shard files.
        size_limit (int): Shard size limit, after which point to start a new shard.
        in_files (List[str]): List of input files to generate arguments for.
    Returns:
        Iterator[Tuple[str, str, str, List[str], int]]: Each argument tuple.
    """
    for in_file in in_files:
        assert in_file.startswith(in_root)
        assert in_file.endswith('.jsonl.xz')
        name = in_file[len(in_root) + 1 : -len('.jsonl.xz')]  # train.eoir
        name = name.replace('.', os.path.sep)  # train/eoir
        sub_out_dir, name = name.split(os.path.sep)[0], name.split(os.path.sep)[1]
        out_dir = os.path.join(out_root, sub_out_dir, name)
        yield in_file, out_dir, compression, hashes, size_limit


def file_to_dir(args: Tuple[str, str, str, List[str], int]) -> Dict[str, int]:
    """Convert a JSONL input file into a directory of MDS shards.
    This is the unit of work executed by the process pool.
    Args:
        args (Tuple[str, str, str, List[str], int): All arguments, packed into a tuple because
            process pools only pass one argument.
    Returns:
        Dict[str, int]: Count of how many samples belonged to each Pile dataset subset.
    """
    in_file, out_dir, compression, hashes, size_limit = args

    columns = {
        'text': 'str',
        # 'pol_set_name': 'str', # can't get this in HF
    }

    counts = Counter()
    with MDSWriter(out_dir, columns, compression, hashes, size_limit) as out:
        for line in lzma.open(open(in_file, 'rb'), 'rt', encoding='utf-8'):
            obj = json.loads(line)
            if obj is None:
                continue
            pol_set_name = out_dir.split(os.path.sep)[-1]
            if pol_set_name[-1].isnumeric():
                # mostly the file name is the set name, but when there is more than one shard per set
                # it has an int suffix, e.g. courtlisteneropinions.7
                pol_set_name = pol_set_name.split('.')[0]
            if sorted(obj.keys()) != ['created_timestamp', 'downloaded_timestamp', 'text', 'url']:
                raise ValueError('Invalid sample fields.')
            text = obj['text']

            sample = {
                'text': text,
                'pol_set_name': pol_set_name,
            }
            out.write(sample)
            counts[pol_set_name] += 1
    return counts


def with_id(basename: str, shard_id: int) -> str:
    """Get a new basename with the given shard_id.
    Args:
        basename (str): Old basename of file.
        shard_id (int): New shard ID.
    Returns:
        str: New basename of file.
    """
    parts = basename.split('.')
    parts[1] = f'{shard_id:05}'
    return '.'.join(parts)


def merge_shard_groups(root: str) -> None:
    """Merge ephemeral sub-datasets created in parallel into one dataset.
    Args:
        root (str): Root directory.
    """
    pattern = os.path.join(root, '*')
    subdirs = sorted(glob(pattern))
    shard_id = 0
    infos = []
    for subdir in subdirs:
        index_filename = os.path.join(subdir, 'index.json')
        obj = json.load(open(index_filename))
        for info in obj['shards']:
            old_basename = info['raw_data']['basename']
            new_basename = with_id(old_basename, shard_id)
            info['raw_data']['basename'] = new_basename

            old_basename = info['zip_data']['basename']
            new_basename = with_id(old_basename, shard_id)
            info['zip_data']['basename'] = new_basename

            old_filename = os.path.join(subdir, old_basename)
            new_filename = os.path.join(root, new_basename)
            assert not os.rename(old_filename, new_filename)

            shard_id += 1
            infos.append(info)

        assert not os.remove(index_filename)
        assert not os.rmdir(subdir)

    index_filename = os.path.join(root, 'index.json')
    obj = {
        'version': 2,
        'shards': infos,
    }
    text = json.dumps(obj, sort_keys=True)
    with open(index_filename, 'w') as out:
        out.write(text)


def main(args: Namespace) -> None:
    """Convert the Pile to streaming format.
    Args:
        args (Namespace): Command-line arguments.
    """
    hashes = get_list_arg(args.hashes)

    # this takes a long time the first time
    ds = datasets.load_dataset("pile-of-law/pile-of-law", "all", cache_dir="hf_pol")
    train_ds = ds['train']
    validation_ds = ds['validation']

    # Get the arguments for each JSONL file conversion.
    arg_tuples = each_task(args.in_root, args.out_root, args.compression, hashes, args.size_limit,
                           in_files)

    # Process each JSONL file in parallel into directories of shards.
    with Pool() as pool:
        counters = pool.imap(file_to_dir, arg_tuples)
        for in_file, counts in zip(in_files, counters):
            obj = {
                'file': in_file,
                'counts': counts,
            }
            print(json.dumps(obj, sort_keys=True))

    # Merge shard groups.
    if (not args.validation_only) or args.train_only:
        train_root = os.path.join(args.out_root, 'train')
        merge_shard_groups(train_root)

    if (not args.train_only) or args.validation_only:
        validation_root = os.path.join(args.out_root, 'validation')
        merge_shard_groups(validation_root)


if __name__ == '__main__':
    main(parse_args())

