import sys
import os
import yaml
import pygame
import locale

from src.utils.logger import Logger

from src.modules.rss.rss_feed import RSSFeed
from src.modules.weather.open_meteo import OpenMeteo,WeatherDataType

from src.display.widgets.simple_label_widget import SimpleLabelWidget
from src.display.widgets.date_widget import DateWidget
from src.display.widgets.time_widget import TimeWidget
from src.display.widgets.horizontal_ticker_widget import HorizontalTickerWidget
from src.display.widgets.month_calendar_widget import MonthCalendarWidget
from src.display.widgets.image_widget import ImageWidget
from src.display.widgets.weather_forecast_widget import WeatherForecastWidget
from src.display.widgets.widget_font import WidgetFont
from src.display.widgets.widget_font_awesome import WidgetFontAwesome, FontAwesomeIcon, FontAwesomeEffect, FontAwesomeEffectSpeed, FontAwesomeSpinEffect, FontAwesomeSpinEffectDirection

configuration_file_path = "config.yaml"

def load_config():
    with open(configuration_file_path, 'r') as file:
        return yaml.safe_load(file)

last_modified_time = os.path.getmtime(configuration_file_path)

config = load_config()

app_name = config.get('general', {}).get('app_name', "Python Smart Home Dashboard")
debug_widgets = config.get('app', {}).get('debug_widgets', False)
max_fps = config.get('app', {}).get('max_fps', 30)
show_fps = config.get('app', {}).get('show_fps', False)
cache_path = config.get('app', {}).get('cache_path', None)
background_color = config.get('app', {}).get('background_color', [0, 0, 0])

locale.setlocale(locale.LC_TIME, config.get('app', {}).get("locale", "en_EN.UTF-8"))
# Inicializar Pygame
pygame.init()

logger = Logger("py-shdb")

# Obtener la resolución actual de la pantalla
screen_info = pygame.display.Info()

logger.debug(f"Current screen resolution: {screen_info.current_w}x{screen_info.current_h}")

RESOLUTION = (screen_info.current_w, screen_info.current_h)

# Configurar pantalla completa
screen = pygame.display.set_mode(RESOLUTION, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.NOFRAME)
pygame.display.set_caption(app_name)

framebuffer_global = pygame.Surface((screen_info.current_w, screen_info.current_h))
framebuffer_global.fill(background_color)

widgets = []

def load_widgets():
    logger.info("Loading widgets")
    widgets.clear()
    for widget_name, widget_config in config.get("widgets", {}).items():
        if (widget_config.get("visible", False)):
            if (widget_config.get("type", "") == "simple_label"):
                logger.debug(f"Adding widget: {widget_name} (SimpleLabelWidget)")
                widgets.append(
                    SimpleLabelWidget(
                        name = widget_name,
                        surface=framebuffer_global,
                        border = debug_widgets,
                        x = widget_config.get('x', 0),
                        y = widget_config.get( 'y', 0),
                        width=widget_config.get( 'width', 0),
                        height=widget_config.get( 'height', 0),
                        padding = widget_config.get( 'padding', 0),
                        background_color = widget_config.get( 'background_color', (0, 0, 0, 0)),
                        font = WidgetFont(
                            family = widget_config.get( 'font_family', None),
                            size = widget_config.get( 'font_size', 30),
                            color = widget_config.get( 'font_color', [255, 255, 255]),
                            style_bold = widget_config.get( 'font_style_bold', False),
                            style_italic = widget_config.get( 'font_style_italic', False)
                        ),
                        text = widget_config.get( 'text', "")
                    )
                )
            elif (widget_config.get("type", "") == "date"):
                widgets.append(
                    DateWidget(
                        name = widget_name,
                        surface=framebuffer_global,
                        border = debug_widgets,
                        x = widget_config.get('x', 0),
                        y = widget_config.get( 'y', 0),
                        width=widget_config.get( 'width', 0),
                        height=widget_config.get( 'height', 0),
                        padding = widget_config.get( 'padding', 0),
                        background_color = widget_config.get( 'background_color', (0, 0, 0, 0)),
                        font = WidgetFont(
                            family = widget_config.get( 'font_family', None),
                            size = widget_config.get( 'font_size', 30),
                            color = widget_config.get( 'font_color', [255, 255, 255]),
                            style_bold = widget_config.get( 'font_style_bold', False),
                            style_italic = widget_config.get( 'font_style_italic', False)
                        ),
                        format_mask = widget_config.get( 'format_mask', "%A, %d de %B"),
                    )
                )
            elif (widget_config.get("type", "") == "time"):
                widgets.append(
                    TimeWidget(
                        name = widget_name,
                        surface=framebuffer_global,
                        border = debug_widgets,
                        x = widget_config.get('x', 0),
                        y = widget_config.get( 'y', 0),
                        width=widget_config.get( 'width', 0),
                        height=widget_config.get( 'height', 0),
                        padding = widget_config.get( 'padding', 0),
                        background_color = widget_config.get( 'background_color', (0, 0, 0, 0)),
                        font = WidgetFont(
                            family = widget_config.get( 'font_family', None),
                            size = widget_config.get( 'font_size', 30),
                            color = widget_config.get( 'font_color', [255, 255, 255]),
                            style_bold = widget_config.get( 'font_style_bold', False),
                            style_italic = widget_config.get( 'font_style_italic', False)
                        ),
                        format_mask = widget_config.get( 'format_mask', "%I:%M %p"),
                    )
                )
            elif (widget_config.get("type", "") == "horizontal_ticker"):
                text = widget_config.get('text', None)
                if text == None or text == "":
                    rss_url = widget_config.get('rss_url', "")
                    if (rss_url != None and rss_url != ""):
                        feed = RSSFeed(url = rss_url, max_items=16, default_seconds_refresh_time= 600,cache_path = cache_path)
                        text = " # ".join(f"[{item['published']}] - {item['title']}" for item in feed.get()['items'])
                widgets.append(
                    HorizontalTickerWidget(
                        name = widget_name,
                        surface=framebuffer_global,
                        border = debug_widgets,
                        x = widget_config.get('x', 0),
                        y = widget_config.get( 'y', 0),
                        width=widget_config.get( 'width', 0),
                        height=widget_config.get( 'height', 0),
                        padding = widget_config.get( 'padding', 0),
                        background_color = widget_config.get( 'background_color', (0, 0, 0, 0)),
                        font = WidgetFont(
                            family = widget_config.get( 'font_family', None),
                            size = widget_config.get( 'font_size', 30),
                            color = widget_config.get( 'font_color', [255, 255, 255]),
                            style_bold = widget_config.get( 'font_style_bold', False),
                            style_italic = widget_config.get( 'font_style_italic', False)
                        ),
                        text = text or "TODO",
                        speed = widget_config.get( 'speed', 1)
                    )
                )
            elif (widget_config.get("type", "") == "month_calendar"):
                widgets.append(
                    MonthCalendarWidget(
                        name = widget_name,
                        surface=framebuffer_global,
                        border = debug_widgets,
                        x = widget_config.get('x', 0),
                        y = widget_config.get( 'y', 0),
                        width=widget_config.get( 'width', 0),
                        height=widget_config.get( 'height', 0),
                        padding = widget_config.get( 'padding', 0),
                        background_color = widget_config.get( 'background_color', (0, 0, 0, 0)),
                        font = WidgetFont(
                            family = widget_config.get( 'font_family', None),
                            size = widget_config.get( 'font_size', 30),
                            color = widget_config.get( 'font_color', [255, 255, 255]),
                            style_bold = widget_config.get( 'font_style_bold', False),
                            style_italic = widget_config.get( 'font_style_italic', False)
                        )
                    )
                )
            elif (widget_config.get("type", "") == "image"):
                widgets.append(
                    ImageWidget(
                        name = widget_name,
                        surface=framebuffer_global,
                        border = debug_widgets,
                        x = widget_config.get('x', 0),
                        y = widget_config.get( 'y', 0),
                        width=widget_config.get( 'width', 0),
                        height=widget_config.get( 'height', 0),
                        padding = widget_config.get( 'padding', 0),
                        background_color = widget_config.get( 'background_color', (0, 0, 0, 0)),
                        path = widget_config.get( 'path', None),
                        url = widget_config.get( 'url', None),
                        cache_path = cache_path
                    )
                )
            elif (widget_config.get("type", "") == "weather_forecast"):
                widgets.append(
                    WeatherForecastWidget(
                        name = widget_name,
                        surface=framebuffer_global,
                        border = debug_widgets,
                        x = widget_config.get('x', 0),
                        y = widget_config.get( 'y', 0),
                        width=widget_config.get( 'width', 0),
                        height=widget_config.get( 'height', 0),
                        padding = widget_config.get( 'padding', 0),
                        background_color = widget_config.get( 'background_color', (0, 0, 0, 0)),
                        font = WidgetFont(
                            #family = widget_config.get( 'font_family', None),
                            file = "resources/fonts/fa-solid-900.ttf",
                            size = widget_config.get( 'font_size', 30),
                            color = widget_config.get( 'font_color', [255, 255, 255]),
                            style_bold = widget_config.get( 'font_style_bold', False),
                            style_italic = widget_config.get( 'font_style_italic', False)
                        ),
                        #text = widget_config.get( 'text', "\uf6c4") # cloud
                        text = widget_config.get( 'text', "\uf013") # fan (wind)
                    )
                )
    logger.debug(f"Total widgets: {len(widgets)}")

load_widgets()

# Fuente para texto e íconos
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)
icon_font = pygame.font.Font("resources/fonts/fa-solid-900.ttf", 32)  # Ruta a tu fuente de íconos (fontawesome)

# fuente para fps
fps_font = pygame.font.SysFont("monospace", 12)

# Reloj para controlar el FPS
clock = pygame.time.Clock()

running = True

widgets_changed = True
previous_fps = -1

click_event = None


wfa1 = FontAwesomeSpinEffect(icon = FontAwesomeIcon.COG, file= "resources/fonts/fa-solid-900.ttf", size= 30, color = (100, 50, 200), speed = FontAwesomeEffectSpeed.SLOW, direction = FontAwesomeSpinEffectDirection.NORMAL)
wfa2 = FontAwesomeSpinEffect(icon = FontAwesomeIcon.COG, file= "resources/fonts/fa-solid-900.ttf", size= 30, color = (100, 50, 200), speed = FontAwesomeEffectSpeed.MEDIUM, direction = FontAwesomeSpinEffectDirection.NORMAL)
wfa3 = FontAwesomeSpinEffect(icon = FontAwesomeIcon.COG, file= "resources/fonts/fa-solid-900.ttf", size= 30, color = (100, 50, 200), speed = FontAwesomeEffectSpeed.FAST, direction = FontAwesomeSpinEffectDirection.NORMAL)

wfa4 = FontAwesomeSpinEffect(icon = FontAwesomeIcon.COG, file= "resources/fonts/fa-solid-900.ttf", size= 30, color = (100, 50, 200), speed = FontAwesomeEffectSpeed.SLOW, direction = FontAwesomeSpinEffectDirection.REVERSED)
wfa5 = FontAwesomeSpinEffect(icon = FontAwesomeIcon.COG, file= "resources/fonts/fa-solid-900.ttf", size= 30, color = (100, 50, 200), speed = FontAwesomeEffectSpeed.MEDIUM, direction = FontAwesomeSpinEffectDirection.REVERSED)
wfa6 = FontAwesomeSpinEffect(icon = FontAwesomeIcon.COG, file= "resources/fonts/fa-solid-900.ttf", size= 30, color = (100, 50, 200), speed = FontAwesomeEffectSpeed.FAST, direction = FontAwesomeSpinEffectDirection.REVERSED)

while running:

    # check for exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            logger.info("See you next time!")
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_event = event

    # DEBUG: check for configuration changes
    if debug_widgets:
        current_modified_time = os.path.getmtime(configuration_file_path)
        if current_modified_time != last_modified_time:
            logger.info("Configuration file changes detected, reloading widgets")
            config = load_config()
            last_modified_time = current_modified_time
            load_widgets()
            framebuffer_global.fill(background_color)
            widgets_changed = True

    for widget in widgets:
        if click_event is not None:
            widget.verify_click(click_event)
        if(widget.refresh(False)):
            widgets_changed = True

    click_event = None

    if show_fps:
        current_fps = int(clock.get_fps())
        if current_fps != previous_fps:
            previous_fps_surface = fps_font.render(f"FPS: {previous_fps:03d}", True, (0, 0, 0))
            previous_fps_rect = previous_fps_surface.get_rect()
            previous_fps_rect.topright = (screen.get_width() - 8, 8)
            framebuffer_global.fill((0, 0, 0), previous_fps_rect)
            current_fps_surface = fps_font.render(f"FPS: {current_fps:03d}", True, (255, 255, 0))
            framebuffer_global.blit(current_fps_surface, (screen.get_width() - current_fps_surface.get_width() - 8, 8))
            previous_fps = current_fps
            widgets_changed = True

    if widgets_changed:
        framebuffer_global.blit(wfa1.animate(), (screen.get_width() - current_fps_surface.get_width() - 100, 50))
        framebuffer_global.blit(wfa2.animate(), (screen.get_width() - current_fps_surface.get_width() - 100, 80))
        framebuffer_global.blit(wfa3.animate(), (screen.get_width() - current_fps_surface.get_width() - 100, 110))
        framebuffer_global.blit(wfa4.animate(), (screen.get_width() - current_fps_surface.get_width() - 100, 140))
        framebuffer_global.blit(wfa5.animate(), (screen.get_width() - current_fps_surface.get_width() - 100, 170))
        framebuffer_global.blit(wfa6.animate(), (screen.get_width() - current_fps_surface.get_width() - 100, 200))
        screen.blit(framebuffer_global, (0, 0))
        widgets_changed = False

    pygame.display.flip()

    # limit FPS
    clock.tick(max_fps)

pygame.quit()

sys.exit()
