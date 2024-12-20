from abc import ABC, abstractmethod
from enum import Enum
import math
import pygame
from .font_awesome_unicode_icons import FontAwesomeUnicodeIcons
from .font_awesome_icon import FontAwesomeIcon

# SIMULATE animations of https://docs.fontawesome.com/web/style/animate#_top
class FontAwesomeAnimation(Enum):
    NONE = 0
    BEAT = 1
    FADE = 2
    BEAT_AND_FADE = 3
    BOUNCE = 4
    HORIZONTAL_FLIP = 5
    VERTICAL_FLIP = 6
    SHAKE = 7
    SPIN_CLOCKWISE = 8
    SPIN_COUNTERCLOCKWISE = 9

class FontAwesomeAnimationSpeed(Enum):
    SLOW = 1
    MEDIUM = 4
    FAST = 8

class FontAwesomeFlipEffectAxis(Enum):
    X = 1
    Y = 2

class FontAwesomeSpinEffectDirection(Enum):
    CLOCKWISE = 1
    COUNTERCLOCKWISE = 2

class FontAwesomeIconBaseEffect(FontAwesomeIcon):
    def __init__(self, icon: FontAwesomeUnicodeIcons, file: str, size: int, color: tuple = (255, 255, 255), background_color: tuple = (0, 0, 0, 0), speed: FontAwesomeAnimationSpeed = FontAwesomeAnimationSpeed.MEDIUM) -> None:
        super().__init__(file = file, size = size, color = color)
        self._animation = FontAwesomeAnimation.NONE
        self._icon = icon
        self._color = color
        self._background_color = background_color
        self._speed = speed.value

class FontAwesomeIconSpinEffect(FontAwesomeIconBaseEffect):
    def __init__(self, icon: FontAwesomeUnicodeIcons, file: str, size: int, color: tuple = (255, 255, 255), background_color: tuple = (0, 0, 0, 0), speed: FontAwesomeAnimationSpeed = FontAwesomeAnimationSpeed.MEDIUM, direction: FontAwesomeSpinEffectDirection = FontAwesomeSpinEffectDirection.CLOCKWISE) -> None:
        super().__init__(icon = icon, file = file, size = size, color = color, speed = speed)
        if direction == FontAwesomeSpinEffectDirection.CLOCKWISE:
            self._animation = FontAwesomeAnimation.SPIN_CLOCKWISE
            self.__angle = 0
        else:
            self._animation = FontAwesomeAnimation.SPIN_COUNTERCLOCKWISE
            self.__angle = 360
        self.__radius = 0
        self.__direction = direction
        self.cache_values()

    def cache_values(self) -> None:
        self.__icon_surface = super().render(self._icon, self._color)
        square_size = max(self.__icon_surface.get_size())
        #self.__sprite_count = 359
        if len(self._background_color) == 4:
            self.__square_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
        else:
            self.__square_surface = pygame.Surface((square_size, square_size))
        self.__center = (self.__icon_surface.get_width() / 2, self.__icon_surface.get_height() / 2)

    def animate(self) -> pygame.Surface:
        x = self.__center[0] + self.__radius * math.cos(math.radians(self.__angle))
        y = self.__center[1] + self.__radius * math.sin(math.radians(self.__angle))
        self.__square_surface.fill((20, 20, 50))
        rotated_icon = pygame.transform.rotate(self.__icon_surface, self.__angle)
        rotated_rect = rotated_icon.get_rect(center=(x, y))
        self.__square_surface.blit(rotated_icon, rotated_rect)
        if self.__direction == FontAwesomeSpinEffectDirection.CLOCKWISE:
            self.__angle = self.__angle - self._speed
            if self.__angle <= 0:
                self.__angle = 360
        else:
            self.__angle = self.__angle + self._speed
            if self.__angle > 360:
                self.__angle = 0
        return self.__square_surface
