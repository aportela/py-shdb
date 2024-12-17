import os
import pickle
import logging
import time
from typing import Any

# Flag to control whether to purge expired caches
PURGE_EXPIRED_CACHES = True

class ModuleCache:
    def __init__(self, cache_path: str = None, expire_seconds: int = 3600):
        """
        Initializes the cache module. Creates the cache directory if necessary.

        :param cache_path: Path to store the cache file. If None, caching is disabled.
        :param expire_seconds: Time in seconds for cache expiration. Default is 3600 seconds (1 hour).
        """
        if cache_path:
            self._cache_path = cache_path
            directory_path = os.path.dirname(self._cache_path)

            try:
                if not os.path.exists(directory_path):
                    logging.warning(f"Cache directory path ({directory_path}) not found. Creating it.")
                    os.makedirs(directory_path, exist_ok=True)
            except Exception as e:
                logging.error(f"Error creating cache directory path ({directory_path}): {e}")
        else:
            logging.warning("Cache path is empty. Disabling cache.")
            self._cache_path = None

        self._expire_seconds = expire_seconds

    def save(self, data: Any):
        """
        Saves the data to the cache file using pickle.

        :param data: The data object to be cached. This can be any Python object.
        """
        if self._cache_path:
            try:
                with open(self._cache_path, "wb") as cache_file:
                    pickle.dump(data, cache_file)
                logging.info(f"Cache saved to ({self._cache_path})")
            except Exception as e:
                logging.error(f"Error saving cache to ({self._cache_path}): {e}")
        else:
            logging.warning("No cache path set. Cannot save cache.")

    def load(self) -> Any:
        """
        Loads the data from the cache file if it's not expired and exists.

        :return: The cached data if available and valid, otherwise None.
        """
        if self._cache_path:
            if os.path.exists(self._cache_path):
                try:
                    # Check if the cache has expired
                    if time.time() - os.path.getmtime(self._cache_path) < self._expire_seconds:
                        with open(self._cache_path, "rb") as cache_file:
                            data = pickle.load(cache_file)
                        logging.info(f"Cache loaded from ({self._cache_path})")
                        return data
                    else:
                        logging.info(f"Cache expired ({self._cache_path})")
                        if PURGE_EXPIRED_CACHES:
                            logging.info(f"Removing expired cache ({self._cache_path})")
                            os.remove(self._cache_path)
                        return None
                except Exception as e:
                    logging.error(f"Error loading cache from ({self._cache_path}): {e}")
                    return None
            else:
                logging.warning(f"Cache file not found ({self._cache_path})")
                return None
        else:
            logging.warning("Cache path is not set. Cannot load cache.")
            return None
