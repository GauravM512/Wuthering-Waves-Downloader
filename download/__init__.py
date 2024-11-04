import os
import sys
import threading
import time
from queue import Queue
import hashlib
from typing import List, Optional
import urllib3
from .models.resources import Model as Resource
from .config import CHUNK_SIZE, DEFAULT_THREADS, DEFAULT_TIMEOUT, MAX_RETRIES

class GameDownloader:
    def __init__(self):
        self.pool = urllib3.PoolManager()

    @staticmethod
    def bytes_to_gb(bytes_value: int) -> float:
        return round(bytes_value / (1024 ** 3), 2)

    def calculate_download_size(self, resource: Resource) -> float:
        return self.bytes_to_gb(sum(x.size for x in resource.resource))

    def _update_progress(self, downloaded: int, file_size: int) -> None:
        percent = 100 * (downloaded / float(file_size))
        filled_length = int(round(50 * downloaded / float(file_size)))
        bar = '█' * filled_length + '-' * (50 - filled_length)
        sys.stdout.write(f'\rProgress: |{bar}| {percent:.1f}% Complete')
        sys.stdout.flush()

    def download_file(self, url: str, output_path: str, num_threads: int = DEFAULT_THREADS) -> bool:
        for attempt in range(MAX_RETRIES):
            try:
                return self._try_download_file(url, output_path, num_threads)
            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    print(f"All download attempts failed for {url}")
                    return False
        return False

    def _try_download_file(self, url: str, output_path: str, num_threads: int) -> bool:
        response = self.pool.request('HEAD', url)
        file_size = int(response.headers.get('content-length', '0'))
        if file_size <= 0:
            raise ValueError("Invalid file size")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'wb') as f:
            f.seek(file_size - 1)
            f.write(b'\0')

        progress: Queue[int] = Queue()
        threads: List[threading.Thread] = []
        
        for i in range(num_threads):
            start = file_size // num_threads * i
            end = file_size // num_threads * (i + 1) - 1 if i < num_threads - 1 else file_size
            thread = threading.Thread(
                target=self._download_chunk,
                args=(url, output_path, start, end, progress)
            )
            thread.start()
            threads.append(thread)

        downloaded = 0
        while downloaded < file_size:
            chunk_size = progress.get(timeout=DEFAULT_TIMEOUT)
            if chunk_size == -1:
                return False
            downloaded += chunk_size
            self._update_progress(downloaded, file_size)

        for thread in threads:
            thread.join()

        print(f"\nDownload completed: {output_path}")
        return True

    def _download_chunk(self, url: str, output_path: str, start_pos: int, end_pos: int, progress: Queue[int]) -> None:
        headers = {'Range': f'bytes={start_pos}-{end_pos}'}
        try:
            with self.pool.request('GET', url, headers=headers, preload_content=False) as response:
                with open(output_path, 'r+b') as file:
                    file.seek(start_pos)
                    for chunk in response.stream(2048):
                        file.write(chunk)
                        progress.put(len(chunk))
        except Exception as e:
            print(f"Chunk download error: {e}")
            progress.put(-1)

    @staticmethod
    def calculate_md5(file_path: str) -> Optional[str]:
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(CHUNK_SIZE), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            print(f"MD5 calculation error for {file_path}: {e}")
            return None

    def verify_and_download(self, resource: Resource, cdn: str, download_path: str) -> None:
        for item in resource.resource:
            file_path = f"{download_path}/{item.dest}"
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            if os.path.exists(file_path):
                if self.calculate_md5(file_path) != item.md5:
                    print(f"Corrupted file: {item.dest}")
                    os.remove(file_path)
                    self.download_file(cdn + item.dest, file_path)
                else:
                    print(f"Verified: {item.dest}")
            else:
                print(f"Downloading: {item.dest}")
                self.download_file(cdn + item.dest, file_path)