from typing import Any, Optional
from abc import ABC, abstractmethod
from datetime import datetime
from ..utils.logger import Logger
from ..modules.cache.cache import ModuleCache

import threading
import queue
import time

from enum import Enum

class DataProviderType(Enum):
    RSS = 1

class DataProvider(ABC):
    def __init__(self, logger: Logger, type: DataProviderType, cache: Optional[ModuleCache] = None) -> None:
        self._log = logger
        self._log.debug(f"Creating new data provider ({type})")
        self.__type = type
        self._cache = cache
        self.__data_queue = queue.Queue(maxsize=1)


    def fetch_data(self, queue):

        new_data = 12 # test data
        # Vaciar la cola antes de poner el nuevo dato
        with queue.mutex:
            self.__data_queue.queue.clear()  # Limpiamos la cola antes de poner el nuevo dato
            self.__data_queue.queue.put(new_data)  # Colocamos el nuevo dato en la cola

        # Vuelve a ejecutar fetch_data cada 2 segundos
        threading.Timer(2, fetch_data, args=(queue)).start()

    @abstractmethod
    def get(self) -> Optional[Any]:
        pass
