import os
import hashlib

from .module_cache import ModuleCache, CacheError
from ..utils.logger import Logger
from .rss.rss_feed import RSSFeed

class RSSCacheError(CacheError):
    """Custom exception for RemoteImageCache-related errors."""
    pass

DEFAULT_EXPIRATION_TIME=300 # 5 min

class RSSCache(ModuleCache):
    def __init__(self, logger: Logger, base_path: str, url: str) -> None:
        super().__init__(logger=logger, base_path=os.path.join(base_path, "feeds"), filename=f"{hashlib.sha256(url.encode('utf-8')).hexdigest()[:64]}.rss", expiration=DEFAULT_EXPIRATION_TIME)
        if not url.startswith(('http://', 'https://')):
            raise ValueError(f"Invalid URL format: {self.__url}")
        self.__url = url
        super()._check()

    def _refresh(self) -> None:
        try:
            rss = RSSFeed(self._log, self.__url)
            rss_data = rss.get(self.__url)
            if not self.save(rss_data):
                raise RSSCacheError(f"Error saving cache of rss from {self.__url}")
        except Exception as e:
            raise RSSCacheError(f"Unexpected error while refreshing cache: {e}")
