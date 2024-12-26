from typing import Optional, Any
from ...utils.logger import Logger
from ..data_provider import DataProvider, DataProviderType
from ...modules.module_cache import ModuleCache
from ...modules.rss.rss_feed import RSSFeed

class RSSDataProvider(DataProvider):
    def __init__(self, logger: Logger, url: str, items: Optional[int] = 16, cache: Optional[ModuleCache] = None,) -> None:
        super().__init__(logger = logger, type = DataProviderType.RSS)
        self.__url = url
        self.__rss = RSSFeed(logger = logger, url = url)

    def get(self) -> Optional[Any]:

        self.__rss.get
        pass