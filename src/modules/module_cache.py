from typing import Any, Optional
from abc import abstractmethod
import os
import pickle
import time
from datetime import datetime
from ..utils.logger import Logger
from pathlib import Path
import threading

class CacheError(Exception):
    """Custom exception for cache-related errors."""
    pass

class ModuleCache:
    def __init__(self, logger: Logger, base_path: str, filename: str, expiration: Optional[int] = None, purge_expired: bool = True) -> None:
        """
        Initialize the cache module.

        :param logger:
            A custom logger instance for logging operations.

        :param expiration:
            The time-to-live (TTL) for the cache, in seconds.
            If set to None, the cache will never expire.

        :param purge_expired:
            If True, expired cache files will be automatically removed when detected.
            If False, expired cache files will remain on the disk.
        """
        self._log = logger
        self.__base_path = os.path.normpath(Path(base_path)) + os.sep
        self.__check_base_path(self.__base_path)
        self.__fullpath = Path(os.path.join(base_path, filename))
        self.__expiration  = expiration
        self.__purge_expired = purge_expired
        self.__last_change = None

    def __check_base_path(self, path: str) -> None:
        """Ensure the cache directory exists."""
        if not os.path.exists(path):
            try:
                self._log.warning(f"Cache directory path ({path}) not found. Creating it.")
                os.makedirs(path, exist_ok=True)
            except Exception as e:
                raise CacheError(f"Error creating cache directory path ({path}): {e}")

    def _purge(self) -> None:
        if os.path.exists(self.__fullpath):
            try:
                self._log.info(f"Removing cache file ({self.__fullpath})")
                os.remove(self.__fullpath)
                self.__last_change = None
            except Exception as e:
                raise CacheError(f"Failed to remove cache file ({self.__fullpath}): {e}")

    @property
    def full_path(self) -> str:
        return self.__fullpath

    @property
    def last_change(self) -> Optional[float]:
        return self.__last_change

    @property
    def exists(self) -> bool:
        return os.path.exists(self.__fullpath)

    @property
    def valid(self) -> bool:
        try:
            # Check if the cache file exists
            if not self.exists:
                self._log.info(f"Cache ({self.__fullpath}) not found.")
                return False

            self._log.info(f"Cache ({self.__fullpath}) found.")

            # If expiration is None, cache never expires
            if self.__expiration is None:
                return True

            # Get the modification time of the cache file
            file_mod_time = os.path.getmtime(self.__fullpath)
            current_time = time.time()

            # Calculate the age of the cache
            cache_age = current_time - file_mod_time
            is_valid = cache_age < self.__expiration

            if not is_valid:
                self._log.info(f"Cache expired. Age: {cache_age}s, Expiration: {self.__expiration}s.")
                if self.__purge_expired:
                    self._purge()
                self.__last_change = None

            self.__last_change = file_mod_time
            return is_valid
        except Exception as e:
            raise CacheError(f"Error checking cache existence/expiration: {e}")

    def save(self, data: Any) -> bool:
        try:
            with open(self.__fullpath, "wb") as cache_file:
                pickle.dump(data, cache_file)
            self.__last_change = datetime.now
            self._log.info(f"Cache saved to ({self.__fullpath})")
            return True
        except Exception as e:
            raise CacheError(f"Error saving cache to ({self.__fullpath}): {e}")

    def save_bytes(self, data: bytes) -> bool:
        if not isinstance(data, bytes):
            self._log.error(f"Expected bytes data, got {type(data)}")
            return False
        try:
            with open(self.__fullpath, "wb") as cache_file:
                cache_file.write(data)
            self.__last_change = datetime.now
            self._log.info(f"Cache saved to ({self.__fullpath})")
            return True
        except Exception as e:
            raise CacheError(f"Error saving cache to ({self.__fullpath}): {e}")

    def load(self) -> Optional[Any]:
        if not self.valid:
            self._log.warning(f"Cache file ({self.__fullpath}) is missing or expired.")
            return None
        try:
            with open(self.__fullpath, "rb") as cache_file:
                data = pickle.load(cache_file)
            self._log.info(f"Cache ({self.__fullpath}) loaded successfully.")
            return data
        except Exception as e:
            raise CacheError(f"Error loading cache ({self.__fullpath}): {e}")

    @abstractmethod
    def _refresh(self, force: bool = False) -> None:
        pass

    def _check(self) -> None:
        if self.__expiration is not None:
                if not self.valid:
                    self._refresh()
                def refresh_periodically():
                    while True:
                        time.sleep(self.__expiration)
                        self._refresh()
                thread = threading.Thread(target=refresh_periodically, daemon=True)
                thread.start()
        else:
            if not self.valid:
                self._refresh()
