import sys
import os
import argparse
import yaml
import pygame
import locale
from typing import Any

from src.utils.logger import Logger

from src.modules.rss.rss_feed import RSSFeed

from src.display.widgets.fps_widget import FPSWidget
from src.display.widgets.simple_label_widget import SimpleLabelWidget
from src.display.widgets.date_widget import DateWidget
from src.display.widgets.time_widget import TimeWidget
from src.display.widgets.horizontal_ticker_widget import HorizontalTickerWidget
from src.display.widgets.month_calendar_widget import MonthCalendarWidget
from src.display.widgets.image_widget import ImageWidget
from src.display.widgets.weather_forecast_widget import WeatherForecastWidget
from src.display.widgets.widget_font import WidgetFont
from src.display.font_awesome_animated_icon import FontAwesomeAnimationSpeed, FontAwesomeAnimationSpinDirection, FontAwesomeIconBeatEffect, FontAwesomeIconBounceEffect, FontAwesomeIconSpinEffect, FontAwesomeIconFlipEffect, FontAwesomeAnimationFlipAxis, FontAwesomeIconFadeEffect, FontAwesomeIconBeatAndFadeEffect
from src.display.font_awesome_unicode_icons import FontAwesomeUnicodeIcons
from src.display.font_awesome_icon import FontAwesomeIcon

from src.display.fps import FPS

logger = Logger("py-shdb")
logger.configure_global(logger.DEBUG)

def parse_args() -> argparse.Namespace:
    logger.debug(f"Commandline args: {sys.argv}")
    parser = argparse.ArgumentParser(description="Parse skin/config custom file.")
    parser.add_argument('-skin', type=str, help='Path to skin/config custom file.', required=False)
    return parser.parse_args()

def load_config(file_path: str) -> Any:
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: skin/config file not found at '{file_path}'.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML format in '{file_path}': {e}")
        sys.exit(1)

COLOR_WHITE=(255, 255, 255)
COLOR_BLACK=(0, 0, 0)

configuration_file_path = "config.yaml"
config = load_config(configuration_file_path)

app_name = config.get('general', {}).get('app_name', "Python Smart Home Dashboard")
debug_widgets = config.get('app', {}).get('debug_widgets', False)
max_fps = config.get('app', {}).get('max_fps', 30)
show_fps = config.get('app', {}).get('show_fps', False)
locale.setlocale(locale.LC_TIME, config.get('app', {}).get("locale", "en_EN.UTF-8"))
cache_path = config.get('app', {}).get('cache_path', None)
skin = config.get('app', {}).get('skin', None)
hide_mouse_cursor = config.get('app', {}).get('hide_mouse_cursor', True)
show_mouse_cursor_on_mouse_motion_events = config.get('app', {}).get('show_mouse_cursor_on_mouse_motion_events', True)
auto_hide_mouse_cursor_timeout = config.get('app', {}).get('auto_hide_mouse_cursor_timeout', 3)

font_awesome_path = config.get('resources', {}).get('font_awesome_path', None)

if font_awesome_path is not None:
    FontAwesomeIcon.set_default_font_filepath(font_awesome_path)

args = parse_args()

if args.skin:
    if not os.path.exists(args.skin):
        print(f"Error: Custom skin/config file '{args.skin}' not found.")
        sys.exit(1)
    skin = args.skin

if skin is None:
    print("Error: skin/config file is empty or invalid.")
    sys.exit(1)

skin_config = load_config(skin)

logger.debug(f"Using skin: {skin}")

last_modified_time = os.path.getmtime(configuration_file_path)

background_image = skin_config.get('skin', {}).get('background_image', None)
background_color = skin_config.get('skin', {}).get('background_color', COLOR_BLACK)

pygame.init()


FPS.set_default_fps(max_fps)

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
screen = pygame.display.set_mode(RESOLUTION, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.NOFRAME)
pygame.display.set_caption(app_name)
"""
if len(background_color) == 4:
    framebuffer_global = pygame.Surface((screen_info.current_w, screen_info.current_h), pygame.SRCALPHA)
else:
    framebuffer_global = pygame.Surface((screen_info.current_w, screen_info.current_h))
"""

framebuffer_global = screen

if background_image is not None:
    if os.path.exists(background_image):
        wallpaper_image = pygame.image.load(background_image)
        wallpaper_scaled = pygame.transform.scale(wallpaper_image, (screen_info.current_w, screen_info.current_h))
        framebuffer_global.blit(wallpaper_scaled, (0, 0))
    else:
        print(f"Error: skin background image '{background_image}' not found.")
        sys.exit(1)
else:
    framebuffer_global.fill(background_color)

pygame.display.flip() # update screen with background color, required becase widgets only update owned area


widgets = []

def load_widgets():
    logger.info("Loading widgets")
    widgets.clear()
    if show_fps:
        widgets.append(
            FPSWidget(
                parent_surface = framebuffer_global,
                name = "fps",
                x = screen_info.current_w - 90,
                y = 8,
                width = 90,
                height = 22,
                padding = 1,
                background_color = None,
                border = debug_widgets,
                font = WidgetFont(
                    family = "monospace",
                    size = 18,
                    color = COLOR_WHITE,
                    style_bold = True,
                    style_italic = False
                )
            )
        )
    for widget_name, widget_config in skin_config.get("skin", {}).get("widgets", {}).items():
        if (widget_config.get("visible", False)):
            if (widget_config.get("type", "") == "simple_label"):
                logger.debug(f"Adding widget: {widget_name} (SimpleLabelWidget)")
                widgets.append(
                    SimpleLabelWidget(
                        parent_surface = framebuffer_global,
                        name = widget_name,
                        x = widget_config.get('x', 0),
                        y = widget_config.get('y', 0),
                        width = widget_config.get('width', 0),
                        height = widget_config.get('height', 0),
                        padding = widget_config.get('padding', 0),
                        background_color = widget_config.get('background_color', None),
                        border = debug_widgets,
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
                        parent_surface = framebuffer_global,
                        name = widget_name,
                        x = widget_config.get('x', 0),
                        y = widget_config.get('y', 0),
                        width = widget_config.get('width', 0),
                        height = widget_config.get('height', 0),
                        padding = widget_config.get('padding', 0),
                        background_color = widget_config.get('background_color', None),
                        border = debug_widgets,
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
                        parent_surface = framebuffer_global,
                        name = widget_name,
                        x = widget_config.get('x', 0),
                        y = widget_config.get('y', 0),
                        width = widget_config.get('width', 0),
                        height = widget_config.get('height', 0),
                        padding = widget_config.get('padding', 0),
                        background_color = widget_config.get('background_color', None),
                        border = debug_widgets,
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
                        feed = RSSFeed(url = rss_url, max_items=16, default_seconds_refresh_time= 600, cache_path = cache_path)
                        text = " # ".join(f"[{item['published']}] - {item['title']}" for item in feed.get()['items'])
                full_width = widget_config.get('full_width', False)
                if full_width:
                    widget_width = screen_info.current_w - 4
                else:
                    widget_width = widget_config.get('width', 0) - 20
                widgets.append(
                    HorizontalTickerWidget(
                        parent_surface = framebuffer_global,
                        name = widget_name,
                        x = 0 if full_width else widget_config.get('x', 0),
                        y = widget_config.get('y', 0),
                        width = widget_width,
                        height = widget_config.get('height', 0),
                        padding = widget_config.get('padding', 0),
                        background_color = widget_config.get('background_color', None),
                        border = debug_widgets,
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
                        parent_surface = framebuffer_global,
                        name = widget_name,
                        x = widget_config.get('x', 0),
                        y = widget_config.get('y', 0),
                        width = widget_config.get('width', 0),
                        height = widget_config.get('height', 0),
                        padding = widget_config.get('padding', 0),
                        background_color = widget_config.get('background_color', None),
                        border = debug_widgets,
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
                        parent_surface = framebuffer_global,
                        name = widget_name,
                        x = widget_config.get('x', 0),
                        y = widget_config.get('y', 0),
                        width = widget_config.get('width', 0),
                        height = widget_config.get('height', 0),
                        padding = widget_config.get('padding', 0),
                        background_color = widget_config.get('background_color', None),
                        border = debug_widgets,
                        path = widget_config.get('path', None),
                        url = widget_config.get('url', None),
                        cache_path = cache_path
                    )
                )
            elif (widget_config.get("type", "") == "weather_forecast"):
                widgets.append(
                    WeatherForecastWidget(
                        parent_surface = framebuffer_global,
                        name = widget_name,
                        x = widget_config.get('x', 0),
                        y = widget_config.get('y', 0),
                        width = widget_config.get('width', 0),
                        height = widget_config.get('height', 0),
                        padding = widget_config.get('padding', 0),
                        background_color = widget_config.get('background_color', None),
                        border = debug_widgets,
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
icon_names = [ FontAwesomeUnicodeIcons.ICON_BASKETBALL, FontAwesomeUnicodeIcons.ICON_SUN, FontAwesomeUnicodeIcons.ICON_COG, FontAwesomeUnicodeIcons.ICON_COMPACT_DISC, FontAwesomeUnicodeIcons.ICON_COMPUTER, FontAwesomeUnicodeIcons.ICON_FROG ]
colors = [ (255, 234, 0), (155, 234, 0), (55, 34, 200) ]
icons = []
icons_size = 30
x = 50
y = 30
for j in range(len(icon_names)):
    for i in range(len(speeds)):
        if j == 0:
            icons.append(
                FontAwesomeIconBounceEffect(parent_surface = framebuffer_global, x = screen.get_width() - x , y = y, icon = icon_names[j], size = icons_size, color = colors[i], background_color = background_color, speed = speeds[i], use_sprite_cache = False)
            )
        elif j == 1:
            icons.append(
                FontAwesomeIconBeatEffect(parent_surface = framebuffer_global, x = screen.get_width() - x , y = y, icon = icon_names[j], size = icons_size, color = colors[i], background_color = background_color, speed = speeds[i], use_sprite_cache = False, max_size = 36)
            )
        elif j == 2:
            icons.append(
                FontAwesomeIconSpinEffect(parent_surface = framebuffer_global, x = screen.get_width() - x , y = y, icon = icon_names[j], size = icons_size, color = colors[i], background_color = background_color, speed = speeds[i], use_sprite_cache = False, direction = FontAwesomeAnimationSpinDirection.CLOCKWISE)
            )
        elif j == 3:
            icons.append(
                FontAwesomeIconFlipEffect(parent_surface = framebuffer_global, x = screen.get_width() - x , y = y, icon = icon_names[j], size = icons_size, color = colors[i], background_color = background_color, speed = speeds[i], use_sprite_cache = False, axis = FontAwesomeAnimationFlipAxis.HORIZONTAL)
            )
        elif j == 4:
                icons.append(
                FontAwesomeIconFadeEffect(parent_surface = framebuffer_global, x = screen.get_width() - x , y = y, icon = icon_names[j], size = icons_size, color = colors[i], background_color = background_color, speed = speeds[i], use_sprite_cache = False)
            )
        elif j == 5:
                icons.append(
                FontAwesomeIconBeatAndFadeEffect(parent_surface = framebuffer_global, x = screen.get_width() - x , y = y, icon = icon_names[j], size = icons_size, color = colors[i], background_color = background_color, speed = speeds[i], use_sprite_cache = False, max_size = 36)
            )
        x += 50
    y += 80
    x = 50

if hide_mouse_cursor:
    pygame.mouse.set_visible(False)

last_mouse_motion_event = pygame.time.get_ticks()
inactive_time = auto_hide_mouse_cursor_timeout * 1000

while running:

    # check for exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            logger.info("See you next time!")
            running = False
        elif event.type == pygame.MOUSEMOTION and show_mouse_cursor_on_mouse_motion_events:
            if not pygame.mouse.get_visible():
                pygame.mouse.set_visible(True)
            last_mouse_motion_event = pygame.time.get_ticks()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_event = event

    # DEBUG: check for configuration changes
    if debug_widgets:
        current_modified_time = os.path.getmtime(configuration_file_path)
        if current_modified_time != last_modified_time:
            # TODO: create method for avoid duplicate code
            logger.info("Configuration file changes detected, reloading widgets")
            config = load_config(configuration_file_path)
            app_name = config.get('general', {}).get('app_name', "Python Smart Home Dashboard")
            debug_widgets = config.get('app', {}).get('debug_widgets', False)
            max_fps = config.get('app', {}).get('max_fps', 30)
            show_fps = config.get('app', {}).get('show_fps', False)
            cache_path = config.get('app', {}).get('cache_path', None)
            background_color = config.get('app', {}).get('background_color', COLOR_BLACK)

            last_modified_time = current_modified_time
            load_widgets()
            framebuffer_global.fill(background_color)
            pygame.display.flip() # update screen with background color, required becase widgets only update owned area
            for widget in widgets:
                widget.refresh_sub_surface_from_parent_surface()

    for widget in widgets:
        if click_event is not None:
            widget.verify_click(click_event)
        widget.refresh(False)

    click_event = None

    # limit fps
    FPS.tick()

    if hide_mouse_cursor and show_mouse_cursor_on_mouse_motion_events:
        current_time = pygame.time.get_ticks()
        if current_time - last_mouse_motion_event > inactive_time:
            if pygame.mouse.get_visible():
                pygame.mouse.set_visible(False)


if hide_mouse_cursor:
    pygame.mouse.set_visible(True)

pygame.quit()

sys.exit()
