from abc import ABC, abstractmethod
from enum import Enum
import math
import pygame
from .widget_font import WidgetFont

class FontAwesomeIcon(Enum):
    COG = "\uf013"

# https://docs.fontawesome.com/web/style/animate#_top
class Effect(Enum):
    NONE = 0
    BEAT = 1
    FADE = 2
    BEAT_AND_FADE = 3
    BOUNCE = 4
    HORIZONTAL_FLIP = 5
    VERTICAL_FLIP = 6
    SHAKE = 7
    SPIN = 8
    SPIN_REVERSE = 9
# https://docs.fontawesome.com/web/style/animate#_top
class FontAwesomeEffect(Enum):
    NONE = 0
    BEAT = 1
    FADE = 2
    BEAT_AND_FADE = 3
    BOUNCE = 4
    HORIZONTAL_FLIP = 5
    VERTICAL_FLIP = 6
    SHAKE = 7
    SPIN = 8
    SPIN_REVERSE = 9

class FontAwesomeEffectSpeed(Enum):
    SLOW = 1
    MEDIUM = 2
    FAST = 4

class FontAwesomeSpinEffectDirection(Enum):
    NORMAL = 1,
    REVERSED = 2


class FontAwesomeBaseEffect(WidgetFont):
    def __init__(self, file: str = None, size: int = 30, color: tuple = (255, 255, 255)) -> None:
        # Initialize the parent class (WidgetFont) with the provided parameters
        super().__init__(file = file, size = size, color = color, style_bold = False, style_italic = False)
        self._effect = Effect.NONE

    @abstractmethod
    def render_animation(self, text: str, custom_color: tuple = None) -> pygame.Surface:
        pass

class FontAwesomeSpinEffect(FontAwesomeBaseEffect):
    def __init__(self, file: str = None, size: int = 30, color: tuple = (255, 255, 255), speed: FontAwesomeEffectSpeed = FontAwesomeEffectSpeed.MEDIUM, direction: FontAwesomeSpinEffectDirection = FontAwesomeSpinEffectDirection.NORMAL) -> None:
        super().__init__(file = file, size = size, color = color)
        self._effect = Effect.BEAT
        self.__radius = 0
        self.__speed = speed.value
        self.__angle = 0
        self.__direction = direction
        if (direction == FontAwesomeSpinEffectDirection.REVERSED):
            self.__angle = 360


    def render_animation(self, icon: FontAwesomeIcon, custom_color: tuple = None) -> pygame.Surface:
        icon_surface = self.render(icon.value, custom_color)
        center = (icon_surface.get_width() / 2, icon_surface.get_height() / 2)
        x = center[0] + self.__radius * math.cos(math.radians(self.__angle))
        y = center[1] + self.__radius * math.sin(math.radians(self.__angle))

        rotated_icon = pygame.transform.rotate(icon_surface, self.__angle)
        rotated_rect = rotated_icon.get_rect(center=(x, y))

        # Conseguimos el tamaño de la superficie original
        icon_width, icon_height = icon_surface.get_size()

        # Calculamos el tamaño cuadrado
        square_size = max(icon_width, icon_height)

        # Creamos una nueva superficie cuadrada
        square_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
        # Render the text using the specified font and blit it to the surface
        square_surface.blit(rotated_icon, rotated_rect)

        if self.__direction == FontAwesomeSpinEffectDirection.NORMAL:
            self.__angle = self.__angle + self.__speed
            if self.__angle > 360:
                self.__angle = 0
        else:
            self.__angle = self.__angle - self.__speed
            if self.__angle >= 0:
                self.__angle = 360
        return square_surface

class WidgetFontAwesome(WidgetFont):
    def __init__(self, file: str = None, size: int = 30, color: tuple = (255, 255, 255)) -> None:
        # Initialize the parent class (WidgetFont) with the provided parameters
        super().__init__(file = file, size = size, color = color, style_bold = False, style_italic = False)

    def render(self, icon: FontAwesomeIcon, effect: FontAwesomeEffect = FontAwesomeEffect.NONE, effect_speed: FontAwesomeEffectSpeed = FontAwesomeEffectSpeed.MEDIUM, custom_color: tuple = None) -> pygame.Surface:
        """Render the specified text as a pygame.Surface."""
        if (effect == FontAwesomeEffect.BEAT):
            return super().render(icon.value, custom_color)
        else:
            return super().render(icon.value, custom_color)
