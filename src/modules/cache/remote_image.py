from typing import Optional
import os
import hashlib
import requests

from .cache import ModuleCache, CacheError

class RemoteImageCacheError(CacheError):
    """Custom exception for RemoteImageCache-related errors."""
    pass

DEFAULT_EXPIRATION_TIME = None # never expires
DEFAULT_TIMEOUT = 10  # seconds

class RemoteImageCache(ModuleCache):
    def __init__(self, base_path: str, url: str, timeout: Optional[int] = DEFAULT_TIMEOUT) -> None:
        super().__init__(base_path=os.path.join(base_path, "images"),
                         filename=f"{hashlib.sha256(url.encode('utf-8')).hexdigest()[:64]}.image",
                         expiration=DEFAULT_EXPIRATION_TIME)
        if not url.startswith(('http://', 'https://')):
            raise ValueError(f"Invalid URL format: {self.__url}")
        self.__url = url
        if timeout <= 0:
            raise ValueError(f"Timeout must be a positive integer: {self.__timeout}")
        self.__timeout = timeout
        super()._check()

    def _refresh(self) -> None:
        try:
            response = requests.get(self.__url, timeout=self.__timeout)
            response.raise_for_status()
            if 'image' not in response.headers['Content-Type']:
                raise ValueError(f"The URL does not point to a valid image: {self.__url}")
            if not self.save_bytes(response.content):
                raise RemoteImageCacheError(f"Error saving cache of remote image from {self.__url}")
        except requests.exceptions.RequestException as e:
            raise RemoteImageCacheError(f"Error fetching image from URL {self.__url}: {e}")
        except ValueError as e:
            raise RemoteImageCacheError(f"Invalid image data: {e}")
        except Exception as e:
            raise RemoteImageCacheError(f"Unexpected error while refreshing cache: {e}")
