import os
import hashlib
import requests

from .module_cache import ModuleCache
from ..utils.logger import Logger

DEFAULT_EXPIRATION_TIME=None # never expires

class RemoteImageCache(ModuleCache):
    def __init__(self, logger: Logger, base_path: str, url: str) -> None:
        super().__init__(logger=logger, base_path=os.path.join(base_path, "images"), filename=f"{hashlib.sha256(url.encode('utf-8')).hexdigest()[:64]}.image", expiration=DEFAULT_EXPIRATION_TIME)
        self.__url = url
        super().check()

    def _refresh(self) -> None:
        try:
            response = requests.get(self.__url, timeout=10)
            response.raise_for_status()
            if 'image' not in response.headers['Content-Type']:
                raise ValueError("The URL does not point to a valid image.")
            if not self.save_bytes(response.content):
                raise ValueError("Error saving cache of remote image.")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error fetching image from URL: {e}")
