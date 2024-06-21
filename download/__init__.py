import sys
import os
import threading
import time
import urllib3
from queue import Queue
from . import url
import hashlib

pool = urllib3.PoolManager()

resource = url.resources()

def bytes_to_gb(bytes_value):
    # 1 GB = 1024^3 bytes
    gb_value = bytes_value / (1024 ** 3)
    rounded_gb_value = round(gb_value, 2)
    return rounded_gb_value

def download_size():
    size= sum([x.size for x in resource.resource])
    return bytes_to_gb(size)

def download_file(url, output_path, num_threads=4, timeout=30):
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

    progress = Queue()
    start_time = time.time()

    try:
        threads = []
        for i in range(num_threads):
            start = file_size // num_threads * i
            end = file_size // num_threads * (i + 1) - 1
            if i == num_threads - 1:
                end = file_size

            thread = threading.Thread(target=_download_chunk, args=(url, output_path, start, end, progress))
            thread.start()
            threads.append(thread)

        downloaded = 0
        while True:
            percent = 100 * (downloaded / float(file_size))
            filled_length = int(round(50 * downloaded / float(file_size)))
            bar = '█' * filled_length + '-' * (50 - filled_length)
            sys.stdout.write(f'\rProgress: |{bar}| {percent:.1f}% Complete')
            sys.stdout.flush()
            
            p = progress.get(True, timeout)
            if p == -1:
                print("\nDownload failed")
                return False
            downloaded += p
            if downloaded >= file_size:
                break

    except Exception as e:
        print(f"\nDownload error: {e}")
        return False

    print(f"\nDownload completed in {time.time() - start_time:.2f} seconds")
    return True

def _download_chunk(url, output_path, start_pos, end_pos, progress):
    headers = {'Range': 'bytes=%d-%d' % (start_pos, end_pos)}
    response = pool.request('GET', url, headers=headers, preload_content=False)
    with open(output_path, 'r+b') as file:
        file.seek(start_pos)
        for chunk in response.stream(2048):
            file.write(chunk)
            progress.put(len(chunk))

def start_download(download_path,threads=4):
    for i in range(len(resource.resource)):
        #check if file exists
        if os.path.exists(f"{download_path}/{resource.resource[i].dest}"):
            continue
        else:
            download_file(url.cdn+resource.resource[i].dest, f"{download_path}/{resource.resource[i].dest}",threads)

def calculate_md5(file_path, chunk_size=1024*1024):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def verify_game(download_path):
    for i in range(len(resource.resource)):
        if os.path.exists(f"{download_path}/{resource.resource[i].dest}"):
            if calculate_md5(f"{download_path}/{resource.resource[i].dest}") == resource.resource[i].md5:
                print(f"{resource.resource[i].dest} is verified")
            else:
                print(f"{resource.resource[i].dest} is corrupted")
                print("deleting corrupted file")
                os.remove(f"{download_path}/{resource.resource[i].dest}")
                download_file(url.cdn+resource.resource[i].dest, f"{download_path}/{resource.resource[i].dest}")
        else:
            print(f"{resource.resource[i].dest} is missing")
            download_file(url.cdn+resource.resource[i].dest, f"{download_path}/{resource.resource[i].dest}")
    print("Verification completed")