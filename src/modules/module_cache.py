from typing import Any, Optional
import os
import pickle
import time
from datetime import datetime
from ..utils.logger import Logger


class CacheError(Exception):
    """Custom exception for cache-related errors."""
    pass


class ModuleCache:
    def __init__(self, logger: Logger, base_path: str, filename: str, expiration: Optional[int] = None, purge_expired: bool = True) -> None:
        """
        Initialize the cache module.

        :param logger:
            A custom logger instance for logging operations.

        :param path:
            The file path where the cached data will be stored.
            It should be a valid path to a writable file location.

        :param expiration:
            The time-to-live (TTL) for the cache, in seconds.
            If set to None, the cache will never expire.

        :param purge_expired:
            If True, expired cache files will be automatically removed when detected.
            If False, expired cache files will remain on the disk.
        """
        self.__log = logger
        self.__base_path = os.path.dirname(base_path)
        self.__check_path()
        self.__fullpath = os.path.join(base_path, filename)
        self.__expiration  = expiration
        self.__purge_expired = purge_expired
        self.__last_change = None
        self.is_cache_valid()

    def __check_path(self, path: str) -> None:
        """Ensure the cache directory exists."""
        if not os.path.exists(path):
            try:
                self.__log.warning(f"Cache directory path ({path}) not found. Creating it.")
                os.makedirs(path, exist_ok=True)
            except Exception as e:
                raise CacheError(f"Error creating cache directory path ({path}): {e}")

    @property
    def is_cached(self) -> bool:
        return os.path.exists(self.__fullpath)

    @property
    def full_cache_path(self) -> str:
        return self.__fullpath

    @property
    def last_change(self) -> Optional[float]:
        return self.__last_change

    def is_cache_valid(self) -> bool:
        """
        Check if the cache is valid based on its expiration time.

        :return:
            True if the cache is valid (not expired or expiration is disabled).
            False if the cache is expired.
        """
        # If expiration is None, cache never expires
        if self.__expiration is None:
            return True

        try:
            # Check if the cache file exists
            if not os.path.exists(self.__fullpath):
                self.__log.info("Cache file does not exist.")
                return False

            # Get the modification time of the cache file
            file_mod_time = os.path.getmtime(self.__fullpath)
            current_time = time.time()

            # Calculate the age of the cache
            cache_age = current_time - file_mod_time
            is_valid = cache_age < self.__expiration

            if not is_valid:
                self.__log.info(f"Cache expired. Age: {cache_age}s, Expiration: {self.__expiration}s.")
                self.__last_change = None

            self.__last_change = file_mod_time
            return is_valid
        except Exception as e:
            self.__log.error(f"Error checking cache validity: {e}")
            return False

    def save(self, data: Any) -> bool:
        """
        Save the data to the cache file using pickle.

        :param data: The data object to be cached. Can be any Python object.
        :return: True if the data was successfully saved, False otherwise.
        """
        try:
            with open(self.__fullpath, "wb") as cache_file:
                pickle.dump(data, cache_file)
            self.__last_change = datetime.now
            self.__log.info(f"Cache saved to ({self.__fullpath})")
            return True
        except Exception as e:
            self.__log.error(f"Error saving cache to ({self.__fullpath}): {e}")
            return False

    def save_bytes(self, data: bytes) -> bool:
        """
        Save raw bytes data to the cache file.

        :param data: The raw bytes to be cached.
        :return: True if the data was successfully saved, False otherwise.
        """
        if not isinstance(data, bytes):
            self.__log.error(f"Expected bytes data, got {type(data)}")
            return False

        try:
            with open(self.__fullpath, "wb") as cache_file:
                cache_file.write(data)
            self.__last_change = datetime.now
            self.__log.info(f"Cache saved to ({self.__fullpath})")
            return True
        except OSError as e:
            self.__log.error(f"Error saving cache to ({self.__fullpath}): {e}")
            return False

    def load(self) -> Optional[Any]:
        """
        Load the data from the cache file if it's valid.

        :return: The cached data if available and valid, otherwise None.
        """
        if not self.is_cache_valid():
            self.__log.warning(f"Cache file is invalid or expired ({self.__fullpath})")
            if self.__purge_expired and os.path.exists(self.__fullpath):
                try:
                    self.__log.info(f"Removing invalid or expired cache file ({self.__fullpath})")
                    os.remove(self.__fullpath)
                    self.__last_change = None
                except Exception as e:
                    self.__log.error(f"Failed to remove expired cache file ({self.__fullpath}): {e}")
            return None

        try:
            with open(self.__fullpath, "rb") as cache_file:
                data = pickle.load(cache_file)
            self.__log.info(f"Cache loaded successfully from ({self.__fullpath})")
            return data
        except Exception as e:
            self.__log.error(f"Error loading cache from ({self.__fullpath}): {e}")
            return None
