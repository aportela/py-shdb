import time
from typing import List, Dict, Any
import requests
from .weather import Weather, WeatherDataType

class OpenMeteo (Weather):
    def __init__(self, latitude: float = 0.0, longitude: float = 0.0, data_interval: WeatherDataType = WeatherDataType.NONE, default_seconds_refresh_time: int = 600):
        super().__init__(latitude=latitude, longitude=longitude, data_interval=data_interval, default_seconds_refresh_time=default_seconds_refresh_time)
        self._api_url = "https://api.open-meteo.com/v1/forecast"
        self._api_params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": "temperature_2m_max,temperature_2m_min,weathercode",
            "timezone": "auto"
        }

    def refresh(self, force: bool = False) -> Dict[str, Any]:
        if force or self.is_data_expired():
            current_time = time.time()
            result = {
                "error": False,    # Default is no errors
                "changed": False,  # Default is no change
                "data": []     # Empty list of articles initially
            }
            if force or current_time - self._last_refresh_timestamp >= self._default_refresh_time:
                try:
                    response = requests.get(self._api_url, params=self._api_params)
                    response.raise_for_status()
                    data = response.json()
                    forecast = data["daily"]
                    return [
                        {
                            "day": i,
                            "temp_max": forecast["temperature_2m_max"][i],
                            "temp_min": forecast["temperature_2m_min"][i],
                            "weather_code": forecast["weathercode"][i]
                        }
                        for i in range(len(forecast["temperature_2m_max"]))
                    ]
                except Exception as e:
                    print("Error fetching weather data:", e)
                    return []
        return result