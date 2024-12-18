import time
from typing import List, Dict, Any
import requests
from .weather import Weather, WeatherDataType
import json

class OpenMeteo (Weather):
    def __init__(self, latitude: float , longitude: float,
                 data_interval: WeatherDataType,
                 default_seconds_refresh_time: int = 600):
        super().__init__(latitude = latitude, longitude = longitude, data_interval = data_interval, default_seconds_refresh_time = default_seconds_refresh_time)
        self._api_url = "https://api.open-meteo.com/v1/forecast"
        self._api_params = {
            "latitude": latitude,
            "longitude": longitude,
            #"daily": "temperature_2m_max,temperature_2m_min,weathercode",
            "hourly": "temperature_2m,precipitation,precipitation_probability,windspeed_10m",
            "timezone": "auto"
        }

    def _get_weather_data(self) -> Dict[str, Any]:
        return None

    def _refresh(self, force: bool = False) -> bool:

        forecast = None
        if self._cache != None:
            forecast = self._cache.load()

        if forecast == None:
            self._log.info("Requesting remote data")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:112.0) Gecko/20100101 Firefox/112.0'
            }

            try:
                response = requests.get(self._api_url, params=self._api_params, headers=headers, timeout=10)
                response.raise_for_status()
                json_data = response.json()
                print(json.dumps(json.loads(json_data)))
            except requests.exceptions.RequestException as e:
                raise RuntimeError(f"Error while fetching forecast: {str(e)}")

            forecast = None # json_data["hourly"]

            if self._cache != None:
                self._cache.save(forecast)
            # Crear la lista con los datos horarios
            self._data = [
                {
                    "hour": forecast["time"][i],  # hour (ISO formatted)
                    "temperature": forecast["temperature_2m"][i],  # Temperature (Celsius)
                    "precipitation_probability": forecast["precipitation_probability"][
                        i],  # precipitation_probability (%)
                    "precipitation": forecast["precipitation"][
                        i],  # precipitation (mm)
                    "windspeed": forecast["windspeed_10m"][i]  # wind speed (km/h)
                }
                for i in range(len(forecast["time"]))  # foreach hour
            ]

            if True:
                self._log.info("New forecast data available!")
                return True  # Return True to indicate the forecast has changed
            else:
                return False
