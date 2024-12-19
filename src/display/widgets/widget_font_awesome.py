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
    MEDIUM = 4
    FAST = 8

class FontAwesomeSpinEffectDirection(Enum):
    NORMAL = 1,
    REVERSED = 2


# TODO: use sprites ?
class FontAwesomeBaseEffect(WidgetFont):
    def __init__(self, file: str = None, size: int = 30, color: tuple = (255, 255, 255)) -> None:
        # Initialize the parent class (WidgetFont) with the provided parameters
        super().__init__(file = file, size = size, color = color, style_bold = False, style_italic = False)
        self._effect = Effect.NONE

    @abstractmethod
    def animate(self) -> pygame.Surface:
        pass

class FontAwesomeSpinEffect(FontAwesomeBaseEffect):
    def __init__(self, icon: FontAwesomeIcon = None, file: str = None, size: int = 30, color: tuple = (255, 255, 255), speed: FontAwesomeEffectSpeed = FontAwesomeEffectSpeed.MEDIUM, direction: FontAwesomeSpinEffectDirection = FontAwesomeSpinEffectDirection.NORMAL) -> None:
        super().__init__(file = file, size = size, color = color)
        if direction == FontAwesomeSpinEffectDirection.NORMAL:
            self._effect = FontAwesomeEffect.SPIN
        else:
            self._effect = FontAwesomeEffect.SPIN_REVERSE
        self.__radius = 0
        self.__speed = speed.value
        self.__angle = 0
        self.__direction = direction
        if (direction == FontAwesomeSpinEffectDirection.REVERSED):
            self.__angle = 360
        self.__icon_surface = self.render(icon.value, color)
        square_size = max(self.__icon_surface.get_size())
        self.__sprite_count = 359
        self.__square_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
        self.__center = (self.__icon_surface.get_width() / 2, self.__icon_surface.get_height() / 2)



    def animate(self) -> pygame.Surface:
        x = self.__center[0] + self.__radius * math.cos(math.radians(self.__angle))
        y = self.__center[1] + self.__radius * math.sin(math.radians(self.__angle))

        self.__square_surface.fill((0,0,0))

        rotated_icon = pygame.transform.rotate(self.__icon_surface, self.__angle)
        rotated_rect = rotated_icon.get_rect(center=(x, y))

        # Render the text using the specified font and blit it to the surface
        self.__square_surface.blit(rotated_icon, rotated_rect)

        if self.__direction == FontAwesomeSpinEffectDirection.NORMAL:
            self.__angle = self.__angle + self.__speed
            if self.__angle > 360:
                self.__angle = 0
        else:
            self.__angle = self.__angle - self.__speed
            if self.__angle <= 0:
                self.__angle = 360
        return self.__square_surface

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
