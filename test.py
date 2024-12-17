import sys
import os
import yaml
import pygame
import locale

from src.display.widgets.simple_label_widget import SimpleLabelWidget
from src.display.widgets.date_widget import DateWidget
from src.display.widgets.time_widget import TimeWidget

configuration_file_path = "config.yaml"

def load_config():
    with open(configuration_file_path, 'r') as file:
        return yaml.safe_load(file)

last_modified_time = os.path.getmtime(configuration_file_path)

config = load_config()


debug = config.get('app', {}).get('debug', False)
max_fps = config.get('app', {}).get('max_fps', 30)
show_fps = config.get('app', {}).get('show_fps', False)
background_color = config.get('app', {}).get('background_color', [0, 0, 0])

locale.setlocale(locale.LC_TIME, config.get('app', {}).get("locale", "en_EN.UTF-8"))
# Inicializar Pygame
pygame.init()

# Obtener la resolución actual de la pantalla
screen_info = pygame.display.Info()
RESOLUTION = (screen_info.current_w, screen_info.current_h)

# Configurar pantalla completa
screen = pygame.display.set_mode(RESOLUTION, pygame.NOFRAME)
pygame.display.set_caption("Weather Forecast and RSS Feed")

framebuffer_global = pygame.Surface((screen_info.current_w, screen_info.current_h))

widgets = []

def load_widgets():
    widgets.clear()
    for widget_name, widget_config in config.get("widgets", {}).items():
        if (widget_config.get("visible", False)):
            if (widget_config.get("type", "") == "simple_label"):
                widgets.append(
                    SimpleLabelWidget(
                        name = widget_name,
                        surface=framebuffer_global,
                        debug = debug,
                        x = widget_config.get('x', 0),
                        y = widget_config.get( 'y', 0),
                        width=widget_config.get( 'width', 0),
                        height=widget_config.get( 'height', 0),
                        padding = widget_config.get( 'padding', 0),
                        font_family = widget_config.get( 'font_family', "monospace"),
                        font_size = widget_config.get( 'font_size', 0),
                        font_color = widget_config.get( 'font_color', [255, 255, 255]),
                        text = widget_config.get( 'text', "")
                    )
                )
            elif (widget_config.get("type", "") == "date"):
                widgets.append(
                    DateWidget(
                        name = widget_name,
                        surface=framebuffer_global,
                        debug = debug,
                        x = widget_config.get('x', 0),
                        y = widget_config.get( 'y', 0),
                        width=widget_config.get( 'width', 0),
                        height=widget_config.get( 'height', 0),
                        padding = widget_config.get( 'padding', 0),
                        font_family = widget_config.get( 'font_family', "monospace"),
                        font_size = widget_config.get( 'font_size', 0),
                        font_color = widget_config.get( 'font_color', [255, 255, 255]),
                        format_mask = widget_config.get( 'format_mask', "%A, %d de %B"),
                    )
                )
            elif (widget_config.get("type", "") == "time"):
                widgets.append(
                    TimeWidget(
                        name = widget_name,
                        surface=framebuffer_global,
                        debug = debug,
                        x = widget_config.get('x', 0),
                        y = widget_config.get( 'y', 0),
                        width=widget_config.get( 'width', 0),
                        height=widget_config.get( 'height', 0),
                        padding = widget_config.get( 'padding', 0),
                        font_family = widget_config.get( 'font_family', "monospace"),
                        font_size = widget_config.get( 'font_size', 0),
                        font_color = widget_config.get( 'font_color', [255, 255, 255]),
                        format_mask = widget_config.get( 'format_mask', "%I:%M %p"),
                    )
                )

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

while running:

    # check for exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # DEBUG: check for configuration changes
    if debug:
        current_modified_time = os.path.getmtime(configuration_file_path)
        if current_modified_time != last_modified_time:
            config = load_config()
            last_modified_time = current_modified_time
            load_widgets()
            framebuffer_global.fill(background_color)
            widgets_changed = True

    for widget in widgets:
        if(widget.refresh(False)):
            widgets_changed = True


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
        screen.blit(framebuffer_global, (0, 0))
        widgets_changed = False

    pygame.display.flip()

    # limit FPS
    clock.tick(max_fps)

pygame.quit()

sys.exit()
