from typing import Any
import os
import pickle
import time
from ..utils.logger import Logger

class ModuleCache:
    def __init__(self, cache_path: str = None, expire_seconds: int = 3600, purge_expired: bool = True):
        self.__log = Logger()
        if cache_path:
            self.__cache_path = cache_path
            directory_path = os.path.dirname(self.__cache_path)
            try:
                if not os.path.exists(directory_path):
                    self.__log.warning(f"Cache directory path ({directory_path}) not found. Creating it.")
                    os.makedirs(directory_path, exist_ok=True)
            except Exception as e:
                self.__log.error(f"Error creating cache directory path ({directory_path}): {e}")
        else:
            self.__log.warning("Cache path is empty. Disabling cache.")
            self.__cache_path = None

        self.__expire_seconds = expire_seconds
        self.__purge_expired = purge_expired

    def save(self, data: Any) -> bool:
        """
        Saves the data to the cache file using pickle.

        :param data: The data object to be cached. This can be any Python object.
        """
        if self.__cache_path:
            try:
                with open(self.__cache_path, "wb") as cache_file:
                    pickle.dump(data, cache_file)
                self.__log.info(f"Cache saved to ({self.__cache_path})")
                return True
            except Exception as e:
                self.__log.error(f"Error saving cache to ({self.__cache_path}): {e}")
                return False
        else:
            self.__log.warning("No cache path set. Cannot save cache.")
            return False

    def save_bytes(self, data: bytes) -> bool:
        """
        Saves raw bytes data to the cache file.

        :param data: The raw bytes to be cached.
        """
        if self.__cache_path:
            try:
                # Open the file in write-binary mode and save the raw bytes data
                with open(self.__cache_path, "wb") as cache_file:
                    cache_file.write(data)
                self.__log.info(f"Cache saved to ({self.__cache_path})")
                return True
            except OSError as e:
                self.__log.error(f"Error saving cache to ({self.__cache_path}): {e}")
                return False
            except Exception as e:
                self.__log.error(f"Unexpected error occurred: {e}")
                return False
        else:
            self.__log.warning("No cache path set. Cannot save cache.")
            return False

    def load(self) -> Any:
        """
        Loads the data from the cache file if it's not expired and exists.

        :return: The cached data if available and valid, otherwise None.
        """
        if self.__cache_path:
            if os.path.exists(self.__cache_path):
                try:
                    # Check if the cache has expired
                    if time.time() - os.path.getmtime(self.__cache_path) < self.__expire_seconds:
                        with open(self.__cache_path, "rb") as cache_file:
                            data = pickle.load(cache_file)
                        self.__log.info(f"Cache loaded from ({self.__cache_path})")
                        return data
                    else:
                        self.__log.info(f"Cache expired ({self.__cache_path})")
                        if self.__purge_expired:
                            self.__log.info(f"Removing expired cache ({self.__cache_path})")
                            os.remove(self.__cache_path)
                        return None
                except Exception as e:
                    self.__log.error(f"Error loading cache from ({self.__cache_path}): {e}")
                    return None
            else:
                self.__log.warning(f"Cache file not found ({self.__cache_path})")
                return None
        else:
            self.__log.warning("Cache path is not set. Cannot load cache.")
            return None
