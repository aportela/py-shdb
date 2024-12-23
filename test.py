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

from src.utils.configuration import Configuration
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
from src.display.icons.font_awesome.animated_icon import FontAwesomeAnimationSpeed, FontAwesomeAnimationSpinDirection, FontAwesomeIconBeatEffect, FontAwesomeIconBounceEffect, FontAwesomeIconSpinEffect, FontAwesomeIconFlipEffect, FontAwesomeAnimationFlipAxis, FontAwesomeIconFadeEffect, FontAwesomeIconBeatAndFadeEffect
from src.display.icons.font_awesome.icon_list import IconList as FontAwesomeIcons
from src.display.icons.font_awesome.icon import Icon as FontAwesomeIcon

from src.display.fps import FPS

logger = Logger("py-shdb")
logger.configure_global(logger.DEBUG)

command_line = Commandline()

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

if command_line.configuration is None:
    configuration_file_path = "config.yaml"
else:
    configuration_file_path = command_line.configuration

config2 = Configuration(configuration_file_path)
config = load_config(configuration_file_path)

skin = config2.skin

if command_line.skin is not None:
    if not os.path.exists(command_line.skin):
        print(f"Error: Custom skin/config file '{command_line.skin}' not found.")
        sys.exit(1)
    skin = command_line.skin

if skin is None:
    print("Error: skin/config file is empty or invalid.")
    sys.exit(1)

skin_config = load_config(skin)

logger.debug(f"Using skin: {skin}")

background_image_url = skin_config.get('skin', {}).get('background_image_url', None)
background_image = skin_config.get('skin', {}).get('background_image', None)
background_color = skin_config.get('skin', {}).get('background_color', COLOR_BLACK)

pygame.init()


screen_info = pygame.display.Info()

logger.debug(f"Current screen resolution: {screen_info.current_w}x{screen_info.current_h}")

skin_width = skin_config.get('skin', {}).get('width', None)
skin_height = skin_config.get('skin', {}).get('height', None)
if ((skin_width, skin_height) != (screen_info.current_w, screen_info.current_h)):
    print(f"Error: skin size (width: {skin_width}px, height: {skin_height}px) do not match with current screen resolution (width: {screen_info.current_w}px, height: {screen_info.current_h}px).")
    sys.exit(1)

RESOLUTION = (screen_info.current_w, screen_info.current_h)

# TODO: check skin resolution match

# Configurar pantalla completa
current_screen_surface = pygame.display.set_mode(size = RESOLUTION, flags = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.NOFRAME, display = config2.monitor_index)
pygame.display.set_caption(config2.app_name)

def set_background_image(path: str):
    if os.path.exists(path):
        wallpaper_image = pygame.image.load(path)
        wallpaper_scaled = pygame.transform.scale(wallpaper_image, (screen_info.current_w, screen_info.current_h))
        current_screen_surface.blit(wallpaper_scaled, (0, 0))
    else:
        print(f"Error: skin background image '{background_image}' not found.")
        sys.exit(1)

def dump_background():

    if background_image_url is not None:
        cache_file_path = f"{config2.cache_path}/images/{hashlib.sha256(background_image_url.encode('utf-8')).hexdigest()[:64]}.image"
        if os.path.exists(cache_file_path):
            logger.debug(f"Remote background url image cache found on {cache_file_path}")
            set_background_image(cache_file_path)
        else:
            try:
                response = requests.get(background_image_url, timeout=10)
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
    elif background_image is not None:
        set_background_image(background_image)
    else:
        current_screen_surface.fill(background_color)

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
    if config2.show_fps:
        widgets.append(
            FPSWidget(
                parent_surface = current_screen_surface,
                name = config.get('widget_defaults', {}).get('fps', {}).get("name", "fps"),
                rect = get_widget_rect_from_config(config.get('widget_defaults', {}).get('fps', {})),
                background_color = None,
                border = config2.debug_widgets,
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
                        border = config2.debug_widgets,
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
                        border = config2.debug_widgets,
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
                        border = config2.debug_widgets,
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
                        feed = RSSFeed(url = rss_url, max_items=16, default_seconds_refresh_time= 600, cache_path = config2.cache_path)
                        text = " # ".join(f"[{item['published']}] - {item['title']}" for item in feed.get()['items'])
                widgets.append(
                    HorizontalTickerWidget(
                        parent_surface = current_screen_surface,
                        name = widget_name,
                        rect = get_widget_rect_from_config(widget_config),
                        background_color = widget_config.get('background_color', None),
                        border = config2.debug_widgets,
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
                        border = config2.debug_widgets,
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
                        border = config2.debug_widgets,
                        path = widget_config.get('path', None),
                        url = widget_config.get('url', None),
                        cache_path = config2.cache_path
                    )
                )
            elif (widget_config.get("type", "") == "weather_forecast"):
                widgets.append(
                    WeatherForecastWidget(
                        parent_surface = current_screen_surface,
                        name = widget_name,
                        rect = get_widget_rect_from_config(widget_config),
                        background_color = widget_config.get('background_color', None),
                        border = config2.debug_widgets,
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

speeds = [ FontAwesomeAnimationSpeed.FAST, FontAwesomeAnimationSpeed.MEDIUM, FontAwesomeAnimationSpeed.SLOW ]
icon_names = [ FontAwesomeIcons.ICON_BASKETBALL, FontAwesomeIcons.ICON_SUN, FontAwesomeIcons.ICON_COG, FontAwesomeIcons.ICON_COMPACT_DISC, FontAwesomeIcons.ICON_COMPUTER, FontAwesomeIcons.ICON_FROG ]
colors = [ (255, 234, 0), (155, 234, 0), (55, 34, 200) ]
icons = []
icons_size = 30
x = 50
y = 30
for j in range(len(icon_names)):
    for i in range(len(speeds)):
        if j == 0:
            icons.append(
                FontAwesomeIconBounceEffect(parent_surface = current_screen_surface, x = current_screen_surface.get_width() - x , y = y, icon = icon_names[j], size = icons_size, color = colors[i], background_color = background_color, speed = speeds[i])
            )
        elif j == 1:
            icons.append(
                FontAwesomeIconBeatEffect(parent_surface = current_screen_surface, x = current_screen_surface.get_width() - x , y = y, icon = icon_names[j], size = icons_size, color = colors[i], background_color = background_color, speed = speeds[i], max_size = 36)
            )
        elif j == 2:
            icons.append(
                FontAwesomeIconSpinEffect(parent_surface = current_screen_surface, x = current_screen_surface.get_width() - x , y = y, icon = icon_names[j], size = icons_size, color = colors[i], background_color = background_color, speed = speeds[i], direction = FontAwesomeAnimationSpinDirection.CLOCKWISE)
            )
        elif j == 3:
            icons.append(
                FontAwesomeIconFlipEffect(parent_surface = current_screen_surface, x = current_screen_surface.get_width() - x , y = y, icon = icon_names[j], size = icons_size, color = colors[i], background_color = background_color, speed = speeds[i], axis = FontAwesomeAnimationFlipAxis.HORIZONTAL)
            )
        elif j == 4:
                icons.append(
                FontAwesomeIconFadeEffect(parent_surface = current_screen_surface, x = current_screen_surface.get_width() - x , y = y, icon = icon_names[j], size = icons_size, color = colors[i], background_color = background_color, speed = speeds[i])
            )
        elif j == 5:
                icons.append(
                FontAwesomeIconBeatAndFadeEffect(parent_surface = current_screen_surface, x = current_screen_surface.get_width() - x , y = y, icon = icon_names[j], size = icons_size, color = colors[i], background_color = background_color, speed = speeds[i], max_size = 36)
            )
        x += 50
    y += 80
    x = 50

if config2.hide_mouse_cursor:
    pygame.mouse.set_visible(False)

last_mouse_motion_event = pygame.time.get_ticks()
inactive_time = config2.auto_hide_mouse_cursor_timeout * 1000

while running:

    # check for exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            logger.info("See you next time!")
            running = False
        elif event.type == pygame.MOUSEMOTION and config2.show_mouse_cursor_on_mouse_motion_events:
            if not pygame.mouse.get_visible():
                pygame.mouse.set_visible(True)
            last_mouse_motion_event = pygame.time.get_ticks()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_event = event

    # DEBUG: check for configuration changes
    if config2.debug_widgets and config2.file_changed:
        # TODO: create method for avoid duplicate code
        logger.info("Configuration file changes detected, reloading widgets")
        config = load_config(configuration_file_path)
        background_color = config.get('app', {}).get('background_color', COLOR_BLACK)
        config2.load()
        config2.apply()
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

    if config2.hide_mouse_cursor and config2.show_mouse_cursor_on_mouse_motion_events:
        current_time = pygame.time.get_ticks()
        if current_time - last_mouse_motion_event > inactive_time:
            if pygame.mouse.get_visible():
                pygame.mouse.set_visible(False)


if config2.hide_mouse_cursor:
    pygame.mouse.set_visible(True)

pygame.quit()

sys.exit()
