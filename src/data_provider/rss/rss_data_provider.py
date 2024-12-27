from typing import Optional, Any
import hashlib
import requests
from ...utils.logger import Logger
from ..data_provider import DataProvider, DataProviderType
from ...modules.cache.cache import ModuleCache
from ...modules.rss.rss_feed import RSSFeed

class RSSDataProvider(DataProvider):
    def __init__(self, logger: Logger, url: str, items: Optional[int] = 16, cache: Optional[ModuleCache] = None) -> None:
        super().__init__(logger = logger, type = DataProviderType.RSS)
        self.__cache = cache
        if cache is not None:
            self._cache_url_hash = ""
        self.__rss = RSSFeed(logger = logger, url = url)

    def __generate_feed_entries_hash(self, entries) -> str:
            """
            Generates a consistent hash based on the unique identifiers (e.g., 'link' or 'guid') of the feed entries.

            :param entries: A list of feed entry dictionaries to hash.
            :return: A SHA-256 hash string representing the feed entries.
            """
            feed_hash = hashlib.sha256()  # Create a new hash object
            for entry in entries:
                feed_hash.update(entry.get("link", "").encode('utf-8'))  # Update the hash with the entry's link
            return feed_hash.hexdigest()  # Return the hex digest of the hash


    def get(self) -> Optional[Any]:
        data = None
        if self.__cache is not None:
             data = self.__cache.load()
        if data is None:
            data = self.__rss.get()
            if self.__cache is not None:
                 self.__cache.save(data)
