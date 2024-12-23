import yaml
from typing import Any
import os
from .logger import Logger

class Configuration:

    __app_name = None
    __debug_widgets = False
    __max_fps = 30
    __show_fps = False

    def __init__(self, path: str):
        self._log = Logger()
        self._log.debug(f"Configuration file: {path}")
        self.__path = path
        self.__loaded_configuration = None

    def load(self, path: str) -> None:
        configuration_path = path if path is None else self.__path
        try:
            with open(configuration_path, 'r') as file:
                self.__loaded_configuration = yaml.safe_load(file)
        except FileNotFoundError:
            raise RuntimeError(f"Error: skin/config file not found at '{configuration_path}'.")
        except yaml.YAMLError as e:
            raise RuntimeError("Error: Invalid YAML format in '{configuration_path}': {e}")
