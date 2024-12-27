import os
import sys
import pygame

from typing import Dict, Any
from .utils.logger import Logger
from .display.fps import FPS
from .utils.commandline import Commandline
from .utils.configuration import AppSettings, SkinSettings
from .modules.remote_image_cache import RemoteImageCache
from .modules.rss_cache import RSSCache

from .display.widgets.fps_widget import FPSWidget
from .display.widgets.simple_label_widget import SimpleLabelWidget
from .display.widgets.date_widget import DateWidget
from .display.widgets.time_widget import TimeWidget
from .display.widgets.horizontal_ticker_widget import HorizontalTickerWidget
from .display.widgets.month_calendar_widget import MonthCalendarWidget
from .display.widgets.image_widget import ImageWidget
from .display.widgets.weather_forecast_widget import WeatherForecastWidget
from .display.widgets.widget_font import WidgetFont

class Boot:
    def __init__(self, ) -> None:
        self.__logger = Logger("py-shdb")
        self.__logger.configure_global(self.__logger.DEBUG)
        # commandline checks
        self.__command_line = Commandline(self.__logger)
        self.__app_settings = None
        # init graphics
        pygame.init()
        self.__screen_info = pygame.display.Info()
        self.__logger.debug(f"Current screen resolution: {self.__screen_info.current_w}x{self.__screen_info.current_h}")
        self.__current_screen_resolution = (self.__screen_info.current_w, self.__screen_info.current_h)
        self.__load_settings_and_skin()
        if (self.__skin_settings.width, self.__skin_settings.height) != self.__current_screen_resolution:
            raise ValueError(f"Error: skin size (width: {self.__skin_settings.width}px, height: {self.__skin_settings.height}px) do not match with current screen resolution (width: {self.__screen_info.current_w}px, height: {self.__screen_info.current_h}px).")
        self.__main_surface = pygame.display.set_mode(size = self.__current_screen_resolution, flags = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.NOFRAME, display = self.__app_settings.monitor_index)
        pygame.display.set_caption(self.__app_settings.app_name)
        self.__refresh_background()
        self.__widgets = []
        self.__load_widgets()

        self.__click_event = None

        if self.__app_settings.hide_mouse_cursor:
            pygame.mouse.set_visible(False)

        self.__last_mouse_motion_event = pygame.time.get_ticks()
        self.__inactive_time = self.__app_settings.auto_hide_mouse_cursor_timeout * 1000
        self.__running = True

    def end(self):
        if self.__app_settings.hide_mouse_cursor:
            pygame.mouse.set_visible(True)
        pygame.quit()

    def __load_settings_and_skin(self) -> None:
        self.__app_settings = AppSettings(self.__logger, self.__command_line.configuration if self.__command_line.configuration is not None else "config.yaml")
        self.__skin_settings = SkinSettings(self.__logger, self.__command_line.skin if self.__command_line.skin is not None else self.__app_settings.skin)

    def __set_background_image(self, path: str) -> None:
        if os.path.exists(path):
            wallpaper_image = pygame.image.load(path)
            wallpaper_scaled = pygame.transform.scale(wallpaper_image, self.__current_screen_resolution)
            self.__main_surface.blit(wallpaper_scaled, (0, 0))
        else:
            raise ValueError(f"Error: skin background image '{path}' not found.")

    def __refresh_background(self) -> None:
        if self.__skin_settings.background_image is not None:
            self.__set_background_image(self.__skin_settings.background_image)
        elif self.__skin_settings.background_image_url is not None:
            try:
                cache = RemoteImageCache(self.__logger, self.__app_settings.cache_path, self.__skin_settings.background_image_url)
                self.__set_background_image(cache.full_path)
            except Exception as e:
                self.__logger.error(f"Error setting remote background image: {e}")
        else:
            self.__main_surface.fill(self.__skin_settings.background_color or pygame.Color("black"))
        pygame.display.flip()

    def get_widget_rect_from_config(self, widget_settings: Dict[str, Any]) -> pygame.Rect:
        position = widget_settings.get('position', None)
        x = widget_settings.get('x', 0)
        y = widget_settings.get('y', 0)
        width = widget_settings.get('width', 0)
        if widget_settings.get('full_width', False):
            width = self.__screen_info.current_w
        height = widget_settings.get('height', 0)
        if widget_settings.get('full_height', False):
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

    def __load_widgets(self):
        self.__logger.info("Loading widgets...")
        self.__widgets.clear()
        if self.__app_settings.show_fps:
            widget_settings = self.__app_settings.get_widget_defaults("fps")
            self.__widgets.append(
                FPSWidget(
                    parent_surface = self.__main_surface,
                    name = widget_settings.get("name", "fps"),
                    rect = self.get_widget_rect_from_config(widget_settings),
                    background_color = None,
                    border = self.__app_settings.debug_widgets,
                    font = WidgetFont(
                        family = widget_settings.get("font_family", "monospace"),
                        size = widget_settings.get("font_size", 18),
                        color = widget_settings.get("font_color", pygame.Color("white")),
                        style_bold = widget_settings.get("font_style_bold", False),
                        style_italic = widget_settings.get("font_style_italic", False),
                    )
                )
            )
        for widget_name, widget_settings in self.__skin_settings.widgets.items():
            if (widget_settings.get("visible", False)):
                if (widget_settings.get("type", None) == "simple_label"):
                    self.__logger.debug(f"Adding widget: {widget_name} (SimpleLabelWidget)")
                    self.__widgets.append(
                        SimpleLabelWidget(
                            parent_surface = self.__main_surface,
                            name = widget_name,
                            rect = self.get_widget_rect_from_config(widget_settings),
                            background_color = widget_settings.get('background_color', None),
                            border = self.__app_settings.debug_widgets,
                            font = WidgetFont(
                                family = widget_settings.get('font_family', None),
                                size = widget_settings.get('font_size', 30),
                                color = widget_settings.get("font_color", pygame.Color("white")),
                                style_bold = widget_settings.get('font_style_bold', False),
                                style_italic = widget_settings.get('font_style_italic', False)
                            ),
                            text = widget_settings.get('text', "")
                        )
                    )
                elif (widget_settings.get("type", None) == "date"):
                    self.__widgets.append(
                        DateWidget(
                            parent_surface = self.__main_surface,
                            name = widget_name,
                            rect = self.get_widget_rect_from_config(widget_settings),
                            background_color = widget_settings.get('background_color', None),
                            border = self.__app_settings.debug_widgets,
                            font = WidgetFont(
                                family = widget_settings.get('font_family', None),
                                size = widget_settings.get('font_size', 30),
                                color = widget_settings.get("font_color", pygame.Color("white")),
                                style_bold = widget_settings.get('font_style_bold', False),
                                style_italic = widget_settings.get('font_style_italic', False)
                            ),
                            format_mask = widget_settings.get('format_mask', "%A, %d de %B"),
                        )
                    )
                elif (widget_settings.get("type", None) == "time"):
                    self.__widgets.append(
                        TimeWidget(
                            parent_surface = self.__main_surface,
                            name = widget_name,
                            rect = self.get_widget_rect_from_config(widget_settings),
                            background_color = widget_settings.get('background_color', None),
                            border = self.__app_settings.debug_widgets,
                            font = WidgetFont(
                                family = widget_settings.get('font_family', None),
                                size = widget_settings.get('font_size', 30),
                                color = widget_settings.get("font_color", pygame.Color("white")),
                                style_bold = widget_settings.get('font_style_bold', False),
                                style_italic = widget_settings.get('font_style_italic', False)
                            ),
                            format_mask = widget_settings.get('format_mask', "%I:%M %p"),
                        )
                    )
                elif (widget_settings.get("type", None) == "horizontal_ticker"):
                    text = None
                    url = widget_settings.get('rss_url', None)
                    if url is not None:
                        try:
                            cache = RSSCache(self.__logger, self.__app_settings.cache_path, url)
                            rss_data = cache.load()
                            item_count = widget_settings.get("rss_item_count", 16)
                            text = " # ".join(f"[{item['published']}] - {item['title']}" for item in rss_data['items'][:item_count])
                        except Exception as e:
                            self.__logger.error(f"Cache error in widget {widget_name} rss ({url})")
                            self.__logger.debug(e)
                    else:
                        text = widget_settings.get('text', None)
                        # TODO: add widget source param (text, rss...)
                        # TODO: pass cache to check changes
                    self.__widgets.append(
                        HorizontalTickerWidget(
                            parent_surface = self.__main_surface,
                            name = widget_name,
                            rect = self.get_widget_rect_from_config(widget_settings),
                            background_color = widget_settings.get('background_color', None),
                            border = self.__app_settings.debug_widgets,
                            font = WidgetFont(
                                family = widget_settings.get('font_family', None),
                                size = widget_settings.get('font_size', 30),
                                color = widget_settings.get("font_color", pygame.Color("white")),
                                style_bold = widget_settings.get('font_style_bold', False),
                                style_italic = widget_settings.get('font_style_italic', False)
                            ),
                            text = text,
                            speed = widget_settings.get('speed', 1)
                        )
                    )
                elif (widget_settings.get("type", None) == "month_calendar"):
                    self.__widgets.append(
                        MonthCalendarWidget(
                            parent_surface = self.__main_surface,
                            name = widget_name,
                            rect = self.get_widget_rect_from_config(widget_settings),
                            background_color = widget_settings.get('background_color', None),
                            border = self.__app_settings.debug_widgets,
                            font = WidgetFont(
                                family = widget_settings.get('font_family', None),
                                size = widget_settings.get('font_size', 30),
                                color = widget_settings.get("font_color", pygame.Color("white")),
                                style_bold = widget_settings.get('font_style_bold', False),
                                style_italic = widget_settings.get('font_style_italic', False)
                            )
                        )
                    )
                elif (widget_settings.get("type", None) == "image"):
                    image_path = None
                    url = widget_settings.get('url', None)
                    if url is not None:
                        try:
                            cache = RemoteImageCache(self.__logger, self.__app_settings.cache_path, url)
                            image_path = cache.full_path
                        except Exception as e:
                            self.__logger.error(f"Cache error in widget {widget_name} remote image ({url})")
                            self.__logger.debug(e)
                    else :
                        image_path = widget_settings.get('path', None)
                    self.__widgets.append(
                        ImageWidget(
                            parent_surface = self.__main_surface,
                            name = widget_name,
                            rect = self.get_widget_rect_from_config(widget_settings),
                            background_color = widget_settings.get('background_color', None),
                            border = self.__app_settings.debug_widgets,
                            path = image_path
                        )
                    )
                elif (False and widget_settings.get("type", None) == "weather_forecast"):
                    self.__widgets.append(
                        WeatherForecastWidget(
                            parent_surface = self.__main_surface,
                            name = widget_name,
                            rect = self.get_widget_rect_from_config(widget_settings),
                            background_color = widget_settings.get('background_color', None),
                            border = self.__app_settings.debug_widgets,
                            font = WidgetFont(
                                family = widget_settings.get('font_family', None),
                                size = widget_settings.get('font_size', 32),
                                color = widget_settings.get("font_color", pygame.Color("white")),
                                style_bold = widget_settings.get('font_style_bold', False),
                                style_italic = widget_settings.get('font_style_italic', False)
                            ),
                            text = widget_settings.get('header_text', 'Weather forecast') # cloud
                        )
                    )
        self.__logger.debug(f"Total widgets: {len(self.__widgets)}")

    def loop(self) -> bool:
        # check for exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.__logger.info("See you next time!")
                return False
            elif event.type == pygame.MOUSEMOTION and self.__app_settings.show_mouse_cursor_on_mouse_motion_events:
                if not pygame.mouse.get_visible():
                    pygame.mouse.set_visible(True)
                self.__last_mouse_motion_event = pygame.time.get_ticks()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.__click_event = event

        # DEBUG: check for configuration changes
        if self.__app_settings.debug_widgets and self.__app_settings.file_changed:
            self.__logger.info("Configuration file changes detected, reloading widgets")
            self.__load_settings_and_skin()
            self.__refresh_background()
            self.__load_widgets()

        for widget in self.__widgets:
            if self.__click_event is not None:
                widget.verify_click(self.__click_event)
            widget.refresh(False)

        self.__click_event = None

        # limit fps
        FPS.tick()

        if self.__app_settings.hide_mouse_cursor and self.__app_settings.show_mouse_cursor_on_mouse_motion_events:
            current_time = pygame.time.get_ticks()
            if current_time - self.__last_mouse_motion_event > self.__inactive_time:
                if pygame.mouse.get_visible():
                    pygame.mouse.set_visible(False)

        return True