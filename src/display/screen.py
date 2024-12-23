from typing import Dict, Any, List
import pygame
from ..utils.configuration import Configuration
from ..utils.logger import Logger

from widgets.fps_widget import FPSWidget
from widgets.simple_label_widget import SimpleLabelWidget
from widgets.date_widget import DateWidget
from widgets.time_widget import TimeWidget
from widgets.horizontal_ticker_widget import HorizontalTickerWidget
from widgets.month_calendar_widget import MonthCalendarWidget
from widgets.image_widget import ImageWidget
from widgets.weather_forecast_widget import WeatherForecastWidget
from widgets.widget_font import WidgetFont

class Screen:

    def __init__(self, configuration: Configuration) -> None:
        self.__log = Logger()
        self.__configuration = configuration
        self.__screen_info = pygame.display.Info()
        self.__screen_resolution = (self.__screen_info.current_w, self.__screen_info.current_h)
        self.__main_surface = pygame.display.set_mode(size = self.__screen_resolution, flags = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.NOFRAME)
        self.__widgets = []
        pygame.display.set_caption(configuration.app_name)

    @property
    def width(self) -> int:
        return self.__screen_info.current_w

    @property
    def height(self) -> int:
        return self.__screen_info.current_h

    def get_widget_rect_from_config(self, widget_config: Dict[str, Any]) -> pygame.Rect:
        position = widget_config.get('position', None)
        x = widget_config.get('x', 0)
        y = widget_config.get('y', 0)
        width = widget_config.get('width', 0)
        if widget_config.get('full_width', False):
            width = self.__screen_info.current_w
        height = widget_config.get('height', 0)
        if widget_config.get('full_height', False):
            height = self.__screen_info.current_h
        if position == "top_left":
            x = 0
            y = 0
        elif position == "top_right":
            x = self.__screen_info.current_w - width
            y = 0
        elif position == "bottom_left":
            x = 0
            y = self.__screen_info.current_h - height
        elif position == "bottom_right":
            x = self.__screen_info.current_w - width
            y = self.__screen_info.current_h - height
        elif position == "center":
            x = ((self.__screen_info.current_w // 2) - (width // 2))
            y = ((self.__screen_info.current_h // 2) - (height // 2))
        elif position == "top_center":
            x = ((self.__screen_info.current_w // 2) - (width // 2))
            y = 0
        elif position == "bottom_center":
            x = ((self.__screen_info.current_w // 2) - (width // 2))
            y = self.__screen_info.current_h - height
        return pygame.Rect(x, y, width, height)

    def load_widgets(self) -> List:
        self.__log.info("Loading widgets")
        current_widget_count = len(self.__widgets)
        if (current_widget_count > 0):
            self.__log.debug(f"Clearing ({current_widget_count}) previous widgets.")
            self.__widgets.clear()
        # TODO
        self.__log.debug(f"Total widgets: {len(self.__widgets)}.")
