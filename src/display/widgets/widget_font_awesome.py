from abc import ABC, abstractmethod
from enum import Enum
import math
import pygame

class FontAwesomeIcon(Enum):
    COG = "\uf013"

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
    SPIN_CLOCKWISE = 8
    SPIN_COUNTERCLOCKWISE = 9

class FontAwesomeEffectSpeed(Enum):
    SLOW = 1
    MEDIUM = 4
    FAST = 8

class FontAwesomeSpinEffectDirection(Enum):
    CLOCKWISE = 1,
    COUNTERCLOCKWISE = 2

# TODO: use sprites ?
class FontAwesomeBaseEffect():
    def __init__(self, file: str = None, size: int = 30, color: tuple = (255, 255, 255)) -> None:
        self._effect = FontAwesomeEffect.NONE
        self.__font = pygame.font.Font(file, size)
        self.__color = color

    def render(self, text: str, custom_color: tuple = None) -> pygame.Surface:
        return self.__font.render(text,  True, (custom_color if custom_color else self.__color))

    @abstractmethod
    def animate(self) -> pygame.Surface:
        pass

class FontAwesomeSpinEffect(FontAwesomeBaseEffect):
    def __init__(self, icon: FontAwesomeIcon = None, file: str = None, size: int = 30, color: tuple = (255, 255, 255), background_color: tuple = (0, 0, 0, 0), speed: FontAwesomeEffectSpeed = FontAwesomeEffectSpeed.MEDIUM, direction: FontAwesomeSpinEffectDirection = FontAwesomeSpinEffectDirection.CLOCKWISE) -> None:
        super().__init__(file = file, size = size, color = color)
        if direction == FontAwesomeSpinEffectDirection.CLOCKWISE:
            self._effect = FontAwesomeEffect.SPIN_CLOCKWISE
            self.__angle = 0
        else:
            self._effect = FontAwesomeEffect.SPIN_COUNTERCLOCKWISE
            self.__angle = 360
        self.__radius = 0
        self.__speed = speed.value
        self.__direction = direction
        self.__icon_surface = self.render(icon.value, color)
        square_size = max(self.__icon_surface.get_size())
        self.__sprite_count = 359
        if len(background_color) == 4:
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
            self.__angle = self.__angle - self.__speed
            if self.__angle <= 0:
                self.__angle = 360
        else:
            self.__angle = self.__angle + self.__speed
            if self.__angle > 360:
                self.__angle = 0
        return self.__square_surface
