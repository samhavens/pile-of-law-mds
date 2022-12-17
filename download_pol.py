import asyncio
import glob
import os
from argparse import ArgumentParser, Namespace
from typing import List

import aiohttp
from tqdm.asyncio import tqdm_asyncio

from pile_of_law_meta import DATA_URL


def parse_args() -> Namespace:
    """Parse command-line arguments.
    Args:
        Namespace: command-line arguments.
    """
    args = ArgumentParser()
    args.add_argument(
        '--download_dir',
        type=str,
        required=False,
        default='data',
        help='Directory path to download the JSONL files to',
    )
    args.add_argument(
        '--max_concurrency',
        type=int,
        default=8,
        help='Number of simultaneous downloads, defaults to 8. Set to -1 to download all simultaneously (untested)',
    )
    args.add_argument(
        '--validation_only',
        action='store_true',
        help='If set, only process the validation split',
    )
    args.add_argument(
        '--train_only',
        action='store_true',
        help='If set, only process the train split',
    )
    args.add_argument(
        '--resume',
        action='store_true',
        help='If set, resume a failed download. WARNING - this may not work as expected',
    )
    return args.parse_args()


async def gather_with_concurrency(n, *coros):
    semaphore = asyncio.Semaphore(n)

    async def sem_coro(coro):
        async with semaphore:
            return await coro
    return await tqdm_asyncio.gather(*(sem_coro(c) for c in coros), total=len(coros))


async def download_file(session, url, dir):
    async with session.get(url) as response:
        filename = os.path.basename(url)
        file_path = os.path.join(dir, filename)
        with open(file_path, 'wb') as f:
            while True:
                chunk = await response.content.read(1024)
                if not chunk:
                    break
                f.write(chunk)
        return file_path


async def download_all_files(urls: List[str], dir: str, max_concurrency: int = 4, timeout_sec: int = 60000):
    """download a list of urls with a certain max_concurrency. Long timeout"""
    timeout = aiohttp.ClientTimeout(total=timeout_sec)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = []
        for url in urls:
            task = asyncio.create_task(download_file(session, url, dir))
            tasks.append(task)

        results = await gather_with_concurrency(max_concurrency, *tasks)
        return results


def resume_urls(all_urls: List[str], downloaded_file_names: List[str]):
    downloaded_no_prefix = {f.split("/")[-1] for f in downloaded_file_names}
    remote_fnames = [f.split("/")[-1] for f in all_urls]
    still_to_fetch = [f for f in remote_fnames if f not in downloaded_no_prefix]
    return still_to_fetch


if __name__ == "__main__":
    args = parse_args()
    download_dir = args.download_dir
    max_concurrency = args.max_concurrency
    train_only = args.train_only
    validation_only = args.validation_only

    os.makedirs(download_dir, exist_ok=True)

    # get all file URLs
    URLS = []
    for subset, splits in DATA_URL.items():
        for split, urls in splits.items():
            for url in urls:
                URLS.append(url)

    if args.resume:
        # if we are resuming, there will be files in the download_dir
        downloaded_files = glob.glob(os.path.join(download_dir, "*.jsonl.xz"))
        if len(downloaded_files):
            urls = resume_urls(URLS, downloaded_files)
            print(f"resuming download. found {len(urls)} remaining files")
            print("note that if a file download was interrupted, this may result in an incomplete version of that file")
            print(f"you might want to kill this process, delete {download_dir} and start again with a higher timeout")
        else:
            print(f"you asked to resume a download but no downloaded files were found")
            exit()
    else:
        urls = URLS

    if train_only:
        urls = [url for url in urls if "train" in url]
    elif validation_only:
        urls = [url for url in urls if "validation" in url]

    if max_concurrency == -1:
        max_concurrency = len(urls)

    print("downloading Pile of Law. Depending on your internet connection, this may take a few hours... or a few minutes.")
    results = asyncio.run(download_all_files(urls, download_dir, max_concurrency=max_concurrency))
    print("saved files:")
    print('\n'.join(results))