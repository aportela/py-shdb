from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import hashlib
import time
from enum import Enum
from ..module_cache import ModuleCache
from ...utils.logger import Logger


class WeatherDataType(Enum):
    """Enum to represent different weather data intervals."""
    NONE = 0
    TODAY = 1
    NEXT_7_DAYS = 2

class Weather(ABC):
    """
    Abstract base class for managing weather data. Subclasses should implement the actual data fetching logic.
    """

    def __init__(self, latitude: float , longitude: float,
                 data_interval: WeatherDataType,
                 default_seconds_refresh_time: int = 600, cache_path: Optional[str] = None):
        """
        Initializes the Weather object with location and refresh settings.

        :param latitude: Latitude of the location.
        :param longitude: Longitude of the location.
        :param data_interval: Time period for weather data (e.g., TODAY, NEXT_7_DAYS).
        :param default_seconds_refresh_time: Time in seconds between automatic refreshes.
        """
        self._log = Logger()
        self._log.debug(f"Using coordinates: {latitude},{longitude} (expire time = {default_seconds_refresh_time} seconds)")
        self._latitude = latitude
        self._longitude = longitude
        self._data_interval = data_interval
        self._default_seconds_refresh_time = default_seconds_refresh_time
        if cache_path != None:
            path = f"{cache_path}/rss/{hashlib.sha256(self._url.encode('utf-8')).hexdigest()}.rss"
            self._cache = ModuleCache(cache_path = path,  expire_seconds = default_seconds_refresh_time, purge_expired = True)
            self._log.debug(f"Cache is enabled: {path}")
        else:
            self._cache = None
            self._log.debug("Cache is disabled")
        self._last_refresh_timestamp = time.time()
        self._data: List[Dict[str, Any]] = []  # Stores fetched weather data
        self._last_data_hash = None  # Hash to detect changes in data

    @abstractmethod
    def _get_weather_data(self) -> Dict[str, Any]:
        """
        Fetches the weather data from a specific source.
        This method should be implemented by child classes.

        :return: A dictionary containing the weather data.
        """
        pass

    @property
    def is_data_expired(self) -> bool:
        """
        Checks if the weather data is expired based on the refresh interval.
        Returns True if the data is expired, otherwise False.

        :return: Boolean indicating if the data is expired.
        """
        return time.time() - self._last_refresh_timestamp >= self._default_seconds_refresh_time

    @abstractmethod
    def _refresh(self, force: bool = False) -> bool:
        """
        Refreshes the weather data from the source.

        :param force: If True, forces the refresh even if the data has not expired.
        :return: Returns True if the refresh was successful, False if there was an error or no new data.
        """
        pass

    def get_data(self, force: bool = False) -> Dict[str, List[Dict[str, str]]]:
        """
        Returns the weather data, refreshing it if necessary.

        :param force: If True, forces the refresh even if the data has not expired.
        :return: A dictionary containing the weather data or an error message if the refresh failed.
        """
        changed = False
        current_time = time.time()  # Get the current time in seconds since the epoch
        if force or current_time - self._last_refresh_timestamp >= self._default_seconds_refresh_time:
            self._log.debug("Forcing new refresh")
            try:
                changed = self._refresh(force)  # Refresh the feed and check if it changed
                self._last_refresh_timestamp = current_time  # Update the timestamp of the last refresh
            except Exception as e:
                raise RuntimeError(f"Error while refreshing forecast: {str(e)}")

        # Return the forecast status and content
        return {
            "changed": changed,
            "data": self._data
        }
