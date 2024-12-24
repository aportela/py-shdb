import sys
import os
import yaml
import pygame

from typing import Dict, Any
import hashlib
import requests

from src.utils.logger import Logger

from src.modules.module_cache import ModuleCache
from src.modules.rss.rss_feed import RSSFeed

from src.utils.configuration import AppSettings, SkinSettings
from src.utils.commandline import Commandline

from src.display.widgets.fps_widget import FPSWidget
from src.display.widgets.simple_label_widget import SimpleLabelWidget
from src.display.widgets.date_widget import DateWidget
from src.display.widgets.time_widget import TimeWidget
from src.display.widgets.horizontal_ticker_widget import HorizontalTickerWidget
from src.display.widgets.month_calendar_widget import MonthCalendarWidget
from src.display.widgets.image_widget import ImageWidget
from src.display.widgets.weather_forecast_widget import WeatherForecastWidget
from src.display.widgets.widget_font import WidgetFont

from src.display.fps import FPS

logger = Logger("py-shdb")
logger.configure_global(logger.DEBUG)

command_line = Commandline(logger)

def load_config(file_path: str) -> Dict[str, Any]:
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: skin/config file not found at '{file_path}'.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML format in '{file_path}': {e}")
        sys.exit(1)

# https://www.pygame.org/docs/ref/color_list.html
COLOR_WHITE = pygame.Color("white")
COLOR_BLACK = pygame.Color("black")

app_settings = AppSettings(logger, command_line.configuration if command_line.configuration is not None else "config.yaml")
config = load_config(command_line.configuration if command_line.configuration is not None else "config.yaml")

skin = app_settings.skin

if command_line.skin is not None:
    if not os.path.exists(command_line.skin):
        print(f"Error: Custom skin/config file '{command_line.skin}' not found.")
        sys.exit(1)
    skin = command_line.skin

if skin is None:
    print("Error: skin/config file is empty or invalid.")
    sys.exit(1)

skin_config = load_config(skin)

skin_settings = SkinSettings(logger, skin)

# TODO: remove
background_color = skin_settings.background_color or COLOR_BLACK

pygame.init()

screen_info = pygame.display.Info()

logger.debug(f"Current screen resolution: {screen_info.current_w}x{screen_info.current_h}")

if ((skin_settings.width, skin_settings.height) != (screen_info.current_w, screen_info.current_h)):
    print(f"Error: skin size (width: {skin_settings.width}px, height: {skin_settings.height}px) do not match with current screen resolution (width: {screen_info.current_w}px, height: {screen_info.current_h}px).")
    sys.exit(1)

RESOLUTION = (screen_info.current_w, screen_info.current_h)

# TODO: check skin resolution match

# Configurar pantalla completa
current_screen_surface = pygame.display.set_mode(size = RESOLUTION, flags = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.NOFRAME, display = app_settings.monitor_index)
pygame.display.set_caption(app_settings.app_name)

def set_background_image(path: str):
    if os.path.exists(path):
        wallpaper_image = pygame.image.load(path)
        wallpaper_scaled = pygame.transform.scale(wallpaper_image, (screen_info.current_w, screen_info.current_h))
        current_screen_surface.blit(wallpaper_scaled, (0, 0))
    else:
        print(f"Error: skin background image '{path}' not found.")
        sys.exit(1)

def dump_background():

    if skin_settings.background_image_url is not None:
        cache_file_path = f"{app_settings.cache_path}/images/{hashlib.sha256(skin_settings.background_image_url.encode('utf-8')).hexdigest()[:64]}.image"
        if os.path.exists(cache_file_path):
            logger.debug(f"Remote background url image cache found on {cache_file_path}")
            set_background_image(cache_file_path)
        else:
            try:
                response = requests.get(skin_settings.background_image_url, timeout=10)
                response.raise_for_status()
                if 'image' not in response.headers['Content-Type']:
                    raise ValueError("The URL does not point to a valid image.")
                cache = ModuleCache(cache_file_path)
                if cache.save_bytes(response.content) is False:
                    raise ValueError("Error saving cache of remote url background image.")
                else:
                    set_background_image(cache_file_path)
            except requests.exceptions.RequestException as e:
                raise ValueError(f"Error fetching image from URL: {e}")
    elif skin_settings.background_image is not None:
        set_background_image(skin_settings.background_image)
    else:
        current_screen_surface.fill(skin_settings.background_color or COLOR_BLACK)

dump_background()
pygame.display.flip() # update screen with background color, required becase widgets only update owned area


widgets = []

def get_widget_rect_from_config(widget_config: Dict[str, Any]) -> pygame.Rect:
    position = widget_config.get('position', None)
    x = widget_config.get('x', 0)
    y = widget_config.get('y', 0)
    width = widget_config.get('width', 0)
    if widget_config.get('full_width', False):
        width = screen_info.current_w
    height = widget_config.get('height', 0)
    if widget_config.get('full_height', False):
        height = screen_info.current_h
    if position == "top_left":
        x = 0
        y = 0
    elif position == "top_right":
        x = screen_info.current_w - width
        y = 0
    elif position == "bottom_left":
        x = 0
        y = screen_info.current_h - height
    elif position == "bottom_right":
        x = screen_info.current_w - width
        y = screen_info.current_h - height
    elif position == "center":
        x = ((screen_info.current_w // 2) - (width // 2))
        y = ((screen_info.current_h // 2) - (height // 2))
    elif position == "top_center":
        x = ((screen_info.current_w // 2) - (width // 2))
        y = 0
    elif position == "bottom_center":
        x = ((screen_info.current_w // 2) - (width // 2))
        y = screen_info.current_h - height
    return pygame.Rect(x, y, width, height)

def load_widgets():
    logger.info("Loading widgets")
    widgets.clear()
    if app_settings.show_fps:
        widgets.append(
            FPSWidget(
                parent_surface = current_screen_surface,
                name = config.get('widget_defaults', {}).get('fps', {}).get("name", "fps"),
                rect = get_widget_rect_from_config(config.get('widget_defaults', {}).get('fps', {})),
                background_color = None,
                border = app_settings.debug_widgets,
                font = WidgetFont(
                    family = config.get('widget_defaults', {}).get('fps', {}).get("font_family", "monospace"),
                    size = config.get('widget_defaults', {}).get('fps', {}).get("font_size", 18),
                    color = config.get('widget_defaults', {}).get('fps', {}).get("font_color", COLOR_WHITE),
                    style_bold = config.get('widget_defaults', {}).get('fps', {}).get("font_style_bold", False),
                    style_italic = config.get('widget_defaults', {}).get('fps', {}).get("font_style_italic", False),
                )
            )
        )
    for widget_name, widget_config in skin_config.get("skin", {}).get("widgets", {}).items():
        if (widget_config.get("visible", False)):
            if (widget_config.get("type", "") == "simple_label"):
                logger.debug(f"Adding widget: {widget_name} (SimpleLabelWidget)")
                widgets.append(
                    SimpleLabelWidget(
                        parent_surface = current_screen_surface,
                        name = widget_name,
                        rect = get_widget_rect_from_config(widget_config),
                        background_color = widget_config.get('background_color', None),
                        border = app_settings.debug_widgets,
                        font = WidgetFont(
                            family = widget_config.get('font_family', None),
                            size = widget_config.get('font_size', 30),
                            color = widget_config.get('font_color', COLOR_WHITE),
                            style_bold = widget_config.get('font_style_bold', False),
                            style_italic = widget_config.get('font_style_italic', False)
                        ),
                        text = widget_config.get( 'text', "")
                    )
                )
            elif (widget_config.get("type", "") == "date"):
                widgets.append(
                    DateWidget(
                        parent_surface = current_screen_surface,
                        name = widget_name,
                        rect = get_widget_rect_from_config(widget_config),
                        background_color = widget_config.get('background_color', None),
                        border = app_settings.debug_widgets,
                        font = WidgetFont(
                            family = widget_config.get('font_family', None),
                            size = widget_config.get('font_size', 30),
                            color = widget_config.get('font_color', COLOR_WHITE),
                            style_bold = widget_config.get('font_style_bold', False),
                            style_italic = widget_config.get('font_style_italic', False)
                        ),
                        format_mask = widget_config.get('format_mask', "%A, %d de %B"),
                    )
                )
            elif (widget_config.get("type", "") == "time"):
                widgets.append(
                    TimeWidget(
                        parent_surface = current_screen_surface,
                        name = widget_name,
                        rect = get_widget_rect_from_config(widget_config),
                        background_color = widget_config.get('background_color', None),
                        border = app_settings.debug_widgets,
                        font = WidgetFont(
                            family = widget_config.get('font_family', None),
                            size = widget_config.get('font_size', 30),
                            color = widget_config.get('font_color', COLOR_WHITE),
                            style_bold = widget_config.get('font_style_bold', False),
                            style_italic = widget_config.get('font_style_italic', False)
                        ),
                        format_mask = widget_config.get('format_mask', "%I:%M %p"),
                    )
                )
            elif (widget_config.get("type", "") == "horizontal_ticker"):
                text = widget_config.get('text', None)
                if text == None or text == "":
                    rss_url = widget_config.get('rss_url', "")
                    if (rss_url != None and rss_url != ""):
                        feed = RSSFeed(url = rss_url, max_items=16, default_seconds_refresh_time= 600, cache_path = app_settings.cache_path)
                        text = " # ".join(f"[{item['published']}] - {item['title']}" for item in feed.get()['items'])
                widgets.append(
                    HorizontalTickerWidget(
                        parent_surface = current_screen_surface,
                        name = widget_name,
                        rect = get_widget_rect_from_config(widget_config),
                        background_color = widget_config.get('background_color', None),
                        border = app_settings.debug_widgets,
                        font = WidgetFont(
                            family = widget_config.get('font_family', None),
                            size = widget_config.get('font_size', 30),
                            color = widget_config.get('font_color', COLOR_WHITE),
                            style_bold = widget_config.get('font_style_bold', False),
                            style_italic = widget_config.get('font_style_italic', False)
                        ),
                        text = text or "TODO",
                        speed = widget_config.get('speed', 1)
                    )
                )
            elif (widget_config.get("type", "") == "month_calendar"):
                widgets.append(
                    MonthCalendarWidget(
                        parent_surface = current_screen_surface,
                        name = widget_name,
                        rect = get_widget_rect_from_config(widget_config),
                        background_color = widget_config.get('background_color', None),
                        border = app_settings.debug_widgets,
                        font = WidgetFont(
                            family = widget_config.get('font_family', None),
                            size = widget_config.get('font_size', 30),
                            color = widget_config.get('font_color', COLOR_WHITE),
                            style_bold = widget_config.get('font_style_bold', False),
                            style_italic = widget_config.get('font_style_italic', False)
                        )
                    )
                )
            elif (widget_config.get("type", "") == "image"):
                widgets.append(
                    ImageWidget(
                        parent_surface = current_screen_surface,
                        name = widget_name,
                        rect = get_widget_rect_from_config(widget_config),
                        background_color = widget_config.get('background_color', None),
                        border = app_settings.debug_widgets,
                        path = widget_config.get('path', None),
                        url = widget_config.get('url', None),
                        cache_path = app_settings.cache_path
                    )
                )
            elif (widget_config.get("type", "") == "weather_forecast"):
                widgets.append(
                    WeatherForecastWidget(
                        parent_surface = current_screen_surface,
                        name = widget_name,
                        rect = get_widget_rect_from_config(widget_config),
                        background_color = widget_config.get('background_color', None),
                        border = app_settings.debug_widgets,
                        font = WidgetFont(
                            family = widget_config.get('font_family', None),
                            size = widget_config.get('font_size', 32),
                            color = widget_config.get('font_color', COLOR_WHITE),
                            style_bold = widget_config.get('font_style_bold', False),
                            style_italic = widget_config.get('font_style_italic', False)
                        ),
                        text = widget_config.get('header_text', 'Weather forecast') # cloud
                    )
                )
    logger.debug(f"Total widgets: {len(widgets)}")

load_widgets()

fps_font = pygame.font.SysFont("monospace", 12)


running = True

click_event = None

if app_settings.hide_mouse_cursor:
    pygame.mouse.set_visible(False)

last_mouse_motion_event = pygame.time.get_ticks()
inactive_time = app_settings.auto_hide_mouse_cursor_timeout * 1000

while running:

    # check for exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            logger.info("See you next time!")
            running = False
        elif event.type == pygame.MOUSEMOTION and app_settings.show_mouse_cursor_on_mouse_motion_events:
            if not pygame.mouse.get_visible():
                pygame.mouse.set_visible(True)
            last_mouse_motion_event = pygame.time.get_ticks()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_event = event

    # DEBUG: check for configuration changes
    if app_settings.debug_widgets and app_settings.file_changed:
        # TODO: create method for avoid duplicate code
        logger.info("Configuration file changes detected, reloading widgets")
        config = load_config(command_line.configuration if command_line.configuration is not None else "config.yaml")
        background_color = config.get('app', {}).get('background_color', COLOR_BLACK)
        app_settings.reload()
        dump_background()
        load_widgets()
        pygame.display.flip() # update screen with background color, required becase widgets only update owned area

    for widget in widgets:
        if click_event is not None:
            widget.verify_click(click_event)
        widget.refresh(False)

    click_event = None

    # limit fps
    FPS.tick()

    if app_settings.hide_mouse_cursor and app_settings.show_mouse_cursor_on_mouse_motion_events:
        current_time = pygame.time.get_ticks()
        if current_time - last_mouse_motion_event > inactive_time:
            if pygame.mouse.get_visible():
                pygame.mouse.set_visible(False)

if app_settings.hide_mouse_cursor:
    pygame.mouse.set_visible(True)

pygame.quit()

sys.exit()
