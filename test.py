import pygame
import sys
import requests
import feedparser

import configparser

# Crear un objeto ConfigParser
config = configparser.ConfigParser()

# Leer el archivo de configuración
config.read('config.ini')

# Inicializar Pygame
pygame.init()

# Obtener la resolución actual de la pantalla
screen_info = pygame.display.Info()
RESOLUTION = (screen_info.current_w, screen_info.current_h)

# Configurar pantalla completa
screen = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN)
pygame.display.set_caption("Weather Forecast and RSS Feed")

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Fuente para texto e íconos
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)
icon_font = pygame.font.Font("resources/fonts/fa-solid-900.ttf", 32)  # Ruta a tu fuente de íconos (fontawesome)

# Reloj para controlar el FPS
clock = pygame.time.Clock()

# URL de la API del tiempo
API_URL = "https://api.open-meteo.com/v1/forecast"
LAT, LON = 40.4168, -3.7038  # Coordenadas de Madrid (puedes cambiarlo)
PARAMS = {
    "latitude": LAT,
    "longitude": LON,
    "daily": "temperature_2m_max,temperature_2m_min,weathercode",
    "timezone": "auto"
}

# URL del feed RSS
RSS_URL = "https://www.meneame.net/rss2.php"

# Obtener datos meteorológicos desde la API
def fetch_weather():
    try:
        response = requests.get(API_URL, params=PARAMS)
        response.raise_for_status()
        data = response.json()
        forecast = data["daily"]
        return [
            {
                "day": i,
                "temp_max": forecast["temperature_2m_max"][i],
                "temp_min": forecast["temperature_2m_min"][i],
                "weather_code": forecast["weathercode"][i]
            }
            for i in range(len(forecast["temperature_2m_max"]))
        ]
    except Exception as e:
        print("Error fetching weather data:", e)
        return []

# Asignar códigos de clima a íconos (usar Unicode de la fuente)
weather_icons = {
    0: "\uf185",  # Soleado (Font Awesome Unicode)
    1: "\uf0c2",  # Nublado
    2: "\uf73d",  # Lluvia
    3: "\uf76c"   # Tormenta
}

def get_weather_icon(code):
    if code == 0:
        return weather_icons[0]
    elif code in [1, 2]:
        return weather_icons[1]
    elif code in [3, 45]:
        return weather_icons[2]
    elif code in [95, 96, 99]:
        return weather_icons[3]
    else:
        return weather_icons[1]

# Obtener los títulos del feed RSS
def fetch_rss_titles(url, max_items=16):
    try:
        feed = feedparser.parse(url)
        return [entry["title"] for entry in feed.entries[:max_items]]
    except Exception as e:
        print("Error fetching RSS feed:", e)
        return ["Error loading RSS feed."]

# Datos iniciales
weather_data = fetch_weather()
rss_titles = fetch_rss_titles(RSS_URL)

# Variables para animar los títulos del RSS
scroll_y = RESOLUTION[1] - 100  # Punto inicial de los títulos
scroll_speed = 1  # Velocidad de desplazamiento

# Bucle principal
running = True
while running:
    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # Dibujar en la pantalla
    screen.fill(BLACK)

    # Dibujar previsión del tiempo en la parte superior
    if weather_data:
        for i, day_data in enumerate(weather_data):
            x = 50 + i * (RESOLUTION[0] // len(weather_data))
            y = RESOLUTION[1] // 8

            # Dibujar ícono del clima
            icon_text = icon_font.render(get_weather_icon(day_data["weather_code"]), True, WHITE)
            screen.blit(icon_text, (x, y))

            # Dibujar texto con temperatura máxima y mínima
            temp_text = font.render(
                f"{day_data['temp_max']}C / {day_data['temp_min']}C", True, WHITE
            )
            screen.blit(temp_text, (x, y + 100))

            # Dibujar el día de la semana
            day_text = font.render(f"Day {day_data['day']+1}", True, WHITE)
            screen.blit(day_text, (x, y - 50))

    else:
        error_text = font.render("Error fetching weather data.", True, RED)
        screen.blit(error_text, (50, 50))

    # Dibujar los títulos del RSS en la parte inferior izquierda
    y = scroll_y
    for title in rss_titles:
        title_text = small_font.render(title, True, WHITE)
        screen.blit(title_text, (20, y))
        y += 30  # Espaciado entre títulos

    # Actualizar la posición para el desplazamiento
    scroll_y -= scroll_speed
    if scroll_y + len(rss_titles) * 30 < 0:
        scroll_y = RESOLUTION[1] - 100

    # Actualizar pantalla
    pygame.display.flip()

    # Controlar FPS

    clock.tick(int(config.get('app', 'max_fps', fallback=60)))

# Salir de Pygame
pygame.quit()
sys.exit()