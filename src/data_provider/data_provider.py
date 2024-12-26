from typing import Any, Optional
from abc import ABC, abstractmethod
from ..utils.logger import Logger
from ..modules.module_cache import ModuleCache

from enum import Enum

class DataProviderType(Enum):
    RSS = 1

class DataProvider(ABC):
    def __init__(self, logger: Logger, type: DataProviderType, cache: Optional[ModuleCache] = None) -> None:
        self._log = logger
        self._log.debug(f"Creating new data provider ({type})")
        self.__type = type
        self._cache = cache

    @abstractmethod
    def get(self) -> Optional[Any]:
        pass
