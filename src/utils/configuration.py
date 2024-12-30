import yaml
import locale
import os
from typing import Optional, Any
from .logger import Logger
from ..display.icons.font_awesome.icon import Icon as FontAwesomeIcon
from ..display.fps import FPS

class Configuration:

    def __init__(self, path: str):
        self._log = Logger()
        self.__path = path
        self._loaded_configuration = None
        self.__last_modified_time = None

    @property
    def file_changed(self) -> bool:
        return os.path.getmtime(self.__path) != self.__last_modified_time

    def _load(self, path: str = None) -> None:
        configuration_path = path if path is not None else self.__path
        try:
            with open(configuration_path, 'r') as file:
                self._loaded_configuration = yaml.safe_load(file)
                self.__last_modified_time = os.path.getmtime(configuration_path)
                self.__path = configuration_path
        except FileNotFoundError:
            raise RuntimeError(f"Error: file not found at '{configuration_path}'.")
        except yaml.YAMLError as e:
            raise RuntimeError("Error: Invalid YAML format in '{configuration_path}': {e}")

class AppSettings (Configuration):

    def __init__(self, path: str):
        super().__init__(path = path)
        self._log.debug(f"Configuration file: {path}")
        super()._load(path)
        self.__apply()

    def __apply(self) -> bool:
        if self._loaded_configuration is not None:
            locale.setlocale(locale.LC_TIME, self._loaded_configuration.get('app', {}).get("locale", "en_EN.UTF-8"))
            FontAwesomeIcon.set_default_font_path(self._loaded_configuration.get('resources', {}).get('font_awesome_path', None))
            FPS.set_default_fps(self._loaded_configuration.get('app', {}).get('max_fps', 30))
            return True
        else:
            return False

    def reload(self) -> bool:
        super()._load()
        return self.__apply()

    @property
    def app_name(self) -> str:
        return self._loaded_configuration.get('app', {}).get('app_name', "Python Smart Home Dashboard")

    @property
    def cache_path(self) -> Optional[str]:
        return self._loaded_configuration.get('app', {}).get('cache_path', None)

    @property
    def show_fps(self) -> bool:
        return self._loaded_configuration.get('app', {}).get('show_fps', False)

    @property
    def debug_widgets(self) -> bool:
        return self._loaded_configuration.get('app', {}).get('debug_widgets', False)

    @property
    def hide_mouse_cursor(self) -> bool:
        return self._loaded_configuration.get('app', {}).get('hide_mouse_cursor', True)

    @property
    def show_mouse_cursor_on_mouse_motion_events(self) -> bool:
        return self._loaded_configuration.get('app', {}).get('show_mouse_cursor_on_mouse_motion_events', True)

    @property
    def auto_hide_mouse_cursor_timeout(self) -> int:
        return self._loaded_configuration.get('app', {}).get('auto_hide_mouse_cursor_timeout', 3)

    @property
    def monitor_index(self) -> int:
        return self._loaded_configuration.get('app', {}).get('monitor_index', 0)

    @property
    def mqtt_broker_url(self) -> Optional[str]:
        return self._loaded_configuration.get('mqtt', {}).get('broker_url', None)

    @property
    def mqtt_username(self) -> Optional[str]:
        return self._loaded_configuration.get('mqtt', {}).get('username', None)

    @property
    def mqtt_password(self) -> Optional[str]:
        return self._loaded_configuration.get('mqtt', {}).get('password', None)

    @property
    def skin(self) -> Optional[str]:
        return self._loaded_configuration.get('app', {}).get('skin', None)

    def get_widget_defaults(self, widget: str) -> Optional[Any]:
        return self._loaded_configuration.get('widget_defaults', {}).get(widget, None)

class SkinSettings (Configuration):

    def __init__(self, path: str):
        super().__init__(path = path)
        self._log.debug(f"Skin file: {path}")
        super()._load(path)

    def reload(self) -> bool:
        super()._load()

    @property
    def background_image_url(self) -> Optional[str]:
        return self._loaded_configuration.get('skin', {}).get('background_image_url', None)

    @property
    def background_image(self) -> Optional[str]:
        return self._loaded_configuration.get('skin', {}).get('background_image', None)

    @property
    def background_color(self) -> Optional[str]:
        return self._loaded_configuration.get('skin', {}).get('background_color', None)

    @property
    def width(self) -> Optional[int]:
        return self._loaded_configuration.get('skin', {}).get('width', None)

    @property
    def height(self) -> Optional[int]:
        return self._loaded_configuration.get('skin', {}).get('height', None)

    @property
    def widgets(self) -> Optional[Any]:
        return self._loaded_configuration.get('skin', {}).get('widgets', {})