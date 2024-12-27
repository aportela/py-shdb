import os
import hashlib

from .module_cache import ModuleCache
from ..utils.logger import Logger
from .rss.rss_feed import RSSFeed

DEFAULT_EXPIRATION_TIME=300 # 5 min

class RSSCache(ModuleCache):
    def __init__(self, logger: Logger, base_path: str, url: str) -> None:
        super().__init__(logger=logger, base_path=os.path.join(base_path, "feeds"), filename=f"{hashlib.sha256(url.encode('utf-8')).hexdigest()[:64]}.rss", expiration=DEFAULT_EXPIRATION_TIME)
        self.__url = url
        super()._check()

    def _refresh(self) -> None:
        rss = RSSFeed(self._log, self.__url)
        try:
            if not self.save(rss.get(self.__url)):
                raise ValueError(f"Error saving rss cache from URL: {self.__url} on path: {self.__fullpath}.")
        except Exception as e:
            raise ValueError(f"Error fetching rss from URL: {self.__url}")
