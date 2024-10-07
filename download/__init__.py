import sys
import os
import threading
import time
import urllib3
from queue import Queue
import hashlib
from typing import List, Optional
from . import url
from .models.resources import Model as Resource
# Initialize the urllib3 PoolManager
pool = urllib3.PoolManager()

def bytes_to_gb(bytes_value: int) -> float:
    """
    Convert bytes to gigabytes, rounded to 2 decimal places.
    """
    return round(bytes_value / (1024 ** 3), 2)

def download_size(resource: Resource) -> float:
    """
    Calculate the total download size of all resources in gigabytes.
    """
    size = sum([x.size for x in resource.resource])
    return bytes_to_gb(size)

def update_progress_bar(downloaded: int, file_size: int) -> None:
    percent = 100 * (downloaded / float(file_size))
    filled_length = int(round(50 * downloaded / float(file_size)))
    bar = '█' * filled_length + '-' * (50 - filled_length)
    sys.stdout.write(f'\rProgress: |{bar}| {percent:.1f}% Complete')
    sys.stdout.flush()

def download_file(url: str, output_path: str, num_threads: int = 4, timeout: int = 30) -> bool:
    """
    Download a file from the given URL to the specified output path using multiple threads.
    """
    try:
        # Get file size from HEAD request
        response = pool.request('HEAD', url)
        file_size = int(response.headers.get('content-length', '0'))
        if file_size <= 0:
            raise ValueError("Invalid file size")
    except Exception as e:
        print(f"Failed to retrieve file size: {e}")
        return False

    print(f"Downloading {url} to {output_path}, size: {file_size} bytes, threads: {num_threads}")

    # Create directories if they don't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Create output file with correct size
    with open(output_path, 'wb') as file:
        file.seek(file_size - 1)
        file.write(b'\0')

    progress: Queue[int] = Queue()
    start_time = time.time()

    try:
        threads: List[threading.Thread] = []
        for i in range(num_threads):
            start = file_size // num_threads * i
            end = file_size // num_threads * (i + 1) - 1
            if i == num_threads - 1:
                end = file_size

            thread = threading.Thread(target=_download_chunk, args=(url, output_path, start, end, progress))
            thread.start()
            threads.append(thread)

        downloaded = 0
        while downloaded < file_size:
            try:
                p = progress.get(timeout=timeout)
                if p == -1:
                    print("\nDownload failed")
                    return False
                downloaded += p
                update_progress_bar(downloaded, file_size)
            except Exception as e:
                print(f"\nDownload error: {e}")
                return False

        for thread in threads:
            thread.join()

    except Exception as e:
        print(f"\nDownload error: {e}")
        return False

    print(f"\nDownload completed in {time.time() - start_time:.2f} seconds")
    return True

def _download_chunk(url: str, output_path: str, start_pos: int, end_pos: int, progress: Queue[int]) -> None:
    """
    Download a chunk of a file from the given URL and write it to the output path.
    """
    headers = {'Range': f'bytes={start_pos}-{end_pos}'}
    try:
        response = pool.request('GET', url, headers=headers, preload_content=False)
        with open(output_path, 'r+b') as file:
            file.seek(start_pos)
            for chunk in response.stream(2048):
                file.write(chunk)
                progress.put(len(chunk))
    except Exception as e:
        print(f"Error downloading chunk {start_pos}-{end_pos}: {e}")
        progress.put(-1)

def start_download(resource: Resource, cdn: str, download_path: str, threads: int = 4) -> None:
    """
    Start downloading all resources to the specified download path using the given number of threads.
    """
    for resource_item in resource.resource:
        dest_path = f"{download_path}{resource_item.dest}"
        download_file(cdn + resource_item.dest, dest_path, threads)
    print("Download completed")

def calculate_md5(file_path: str, chunk_size: int = 1024*1024) -> Optional[str]:
    """
    Calculate the MD5 checksum of a file.
    """
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        print(f"Error calculating MD5 for {file_path}: {e}")
        return None

def verify_game(resource: Resource, cdn: str, download_path: str) -> None:
    """
    Verify the integrity of downloaded game files by comparing their MD5 checksums.
    """
    for resource_item in resource.resource:
        file_path = f"{download_path}/{resource_item.dest}"
        if os.path.exists(file_path):
            calculated_md5 = calculate_md5(file_path)
            if calculated_md5 == resource_item.md5:
                print(f"{resource_item.dest} is verified")
            else:
                print(f"{resource_item.dest} is corrupted. Deleting and re-downloading...")
                os.remove(file_path)
                download_file(cdn + resource_item.dest, file_path)
        else:
            print(f"{resource_item.dest} is missing. Downloading...")
            download_file(cdn + resource_item.dest, file_path)
    print("Verification completed")
