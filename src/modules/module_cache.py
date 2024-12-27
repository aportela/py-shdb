from typing import Any, Optional
from abc import abstractmethod
import os
import pickle
import time
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

        :param logger: A custom logger instance for logging operations.
        :param base_path: The base directory where cache files are stored.
        :param filename: The name of the cache file.
        :param expiration: Time-to-live (TTL) for the cache, in seconds. If None, the cache never expires.
        :param purge_expired: If True, expired cache files will be automatically removed.
        """
        self._log = logger
        self.__base_path = os.path.normpath(Path(base_path)) + os.sep
        self.__check_base_path(self.__base_path)
        self.__fullpath = Path(os.path.join(base_path, filename))
        self.__expiration = expiration
        self.__purge_expired = purge_expired
        self.__last_change = None

    def __check_base_path(self, path: str) -> None:
        """Ensure the cache directory exists. Create it if it doesn't exist."""
        if not os.path.exists(path):
            try:
                self._log.warning(f"Cache directory path ({path}) not found. Creating it.")
                os.makedirs(path, exist_ok=True)
            except Exception as e:
                raise CacheError(f"Error creating cache directory path ({path}): {e}")

    def _purge(self) -> None:
        """Delete the cache file if it exists."""
        if os.path.exists(self.__fullpath):
            try:
                self._log.info(f"Removing cache file ({self.__fullpath})")
                os.remove(self.__fullpath)
                self.__last_change = None
            except Exception as e:
                raise CacheError(f"Failed to remove cache file ({self.__fullpath}): {e}")

    @property
    def full_path(self) -> str:
        """Get the full path to the cache file."""
        return self.__fullpath

    @property
    def last_change(self) -> Optional[float]:
        """Get the last modification timestamp of the cache."""
        return self.__last_change

    @property
    def exists(self) -> bool:
        """Check if the cache file exists."""
        try:
            return os.path.exists(self.__fullpath)
        except Exception as e:
            self._log.error(f"Error checking if cache file exists: {e}")
            return False

    @property
    def valid(self) -> bool:
        """
        Check if the cache file is valid.

        Returns:
            True if the cache exists and has not expired; otherwise, False.
        """
        try:
            if not self.exists:
                self._log.info(f"Cache ({self.__fullpath}) not found.")
                return False

            self._log.info(f"Cache ({self.__fullpath}) found.")

            if self.__expiration is None:
                return True

            file_mod_time = os.path.getmtime(self.__fullpath)
            current_time = time.time()

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
        """
        Save data to the cache file using pickle serialization.

        :param data: The data to be cached.
        :return: True if the data was saved successfully, otherwise False.
        """
        try:
            with open(self.__fullpath, "wb") as cache_file:
                pickle.dump(data, cache_file)
            self.__last_change = time.time()
            self._log.info(f"Cache saved to ({self.__fullpath})")
            return True
        except Exception as e:
            raise CacheError(f"Error saving cache to ({self.__fullpath}): {e}")

    def save_bytes(self, data: bytes) -> bool:
        """
        Save raw bytes to the cache file.

        :param data: Bytes to be saved in the cache.
        :return: True if the bytes were saved successfully, otherwise False.
        """
        if not isinstance(data, bytes):
            self._log.error(f"Expected bytes data, got {type(data)}")
            return False
        try:
            with open(self.__fullpath, "wb") as cache_file:
                cache_file.write(data)
            self.__last_change = time.time()
            self._log.info(f"Cache saved to ({self.__fullpath})")
            return True
        except Exception as e:
            raise CacheError(f"Error saving cache to ({self.__fullpath}): {e}")

    def load(self) -> Optional[Any]:
        """
        Load data from the cache file using pickle deserialization.

        :return: The cached data if it exists and is valid; otherwise, None.
        """
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
        """
        Abstract method for refreshing the cache.

        Subclasses should implement this method to define the cache refresh behavior.
        """
        pass

    def _check(self) -> None:
        """
        Check the validity of the cache and refresh it periodically if expiration is set.

        If expiration is None, the cache will only be refreshed if it's invalid.
        """
        def refresh_periodically(stop_event):
            while not stop_event.is_set():
                time.sleep(self.__expiration)
                self._refresh()

        if self.__expiration is not None:
            if not self.valid:
                self._refresh()
            if not hasattr(self, "_stop_event"):
                self._stop_event = threading.Event()
                thread = threading.Thread(target=refresh_periodically, args=(self._stop_event,), daemon=True)
                thread.start()
        else:
            if not self.valid:
                self._refresh()