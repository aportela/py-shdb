import os
import hashlib

from .cache import ModuleCache, CacheError
from ..rss.rss_feed import RSSFeed

class RSSCacheError(CacheError):
    """Custom exception for RemoteImageCache-related errors."""
    pass

DEFAULT_EXPIRATION_TIME=300 # 5 min

class RSSCache(ModuleCache):
    def __init__(self, base_path: str, url: str) -> None:
        super().__init__(base_path=os.path.join(base_path, "feeds"), filename=f"{hashlib.sha256(url.encode('utf-8')).hexdigest()[:64]}.rss", expiration=DEFAULT_EXPIRATION_TIME)
        if not url.startswith(('http://', 'https://')):
            raise ValueError(f"Invalid URL format: {self.__url}")
        self.__url = url
        super()._check()

    def _refresh(self) -> None:
        try:
            rss = RSSFeed(url = self.__url)
            rss_data = rss.get()
            if not self.save(rss_data):
                raise RSSCacheError(f"Error saving cache of rss from {self.__url}")
        except Exception as e:
            raise RSSCacheError(f"Unexpected error while refreshing cache: {e}")
