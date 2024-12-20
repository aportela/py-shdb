from abc import abstractmethod
from enum import Enum
import math
import pygame
from .font_awesome_unicode_icons import FontAwesomeUnicodeIcons
from .font_awesome_icon import FontAwesomeIcon

# SIMULATE animations of https://docs.fontawesome.com/web/style/animate#_top
class FontAwesomeAnimationType(Enum):
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

class FontAwesomeAnimationFlipAxis(Enum):
    X = 1
    Y = 2

class FontAwesomeAnimationSpinDirection(Enum):
    CLOCKWISE = 1
    COUNTERCLOCKWISE = 2

class FontAwesomeIconBaseEffect(FontAwesomeIcon):
    def __init__(self, icon: FontAwesomeUnicodeIcons, file: str, size: int, color: tuple[int, int, int] = (255, 255, 255), background_color: tuple[int, int, int, int] = (0, 0, 0, 0), speed: FontAwesomeAnimationSpeed = FontAwesomeAnimationSpeed.MEDIUM, use_sprite_cache: bool = False) -> None:
        super().__init__(file = file, size = size, color = color)
        self._animation_type = FontAwesomeAnimationType.NONE
        self._icon = icon
        self._color = color
        self._background_color = background_color
        self._speed = speed.value
        self._use_sprite_cache = use_sprite_cache
        self._tmp_surface = None

    def __clear(self):
        self._tmp_surface.fill(self.__background_color)

    def set_surface(self, surface: pygame.Surface, x: int, y: int, width: int, height: int, padding: int, background_color: tuple[int, int, int, int] = (0, 0, 0, 0)) -> None:
        self._surface = surface
        self.__x = x
        self.__y = y
        if width < 1 or height < 1 or padding < 0:
            raise ValueError("Invalid width/height/padding.")
        self.__width = width
        self.__height = height
        self.__padding = padding
        self.__background_color = background_color

    def animate_on_surface(self) -> None:
        if self._surface and self._tmp_surface:
            self._surface.blit(self._tmp_surface, (self.__x, self.__y))
            self.__clear()

    @abstractmethod
    def _cache_values(self) -> None:
        pass

    @abstractmethod
    def animate(self) -> pygame.Surface:
        pass

class FontAwesomeIconBeatEffect(FontAwesomeIconBaseEffect):
    def __init__(self, icon: FontAwesomeUnicodeIcons, file: str, size: int, color: tuple[int, int, int] = (255, 255, 255), background_color: tuple[int, int, int, int] = (0, 0, 0, 0), speed: FontAwesomeAnimationSpeed = FontAwesomeAnimationSpeed.MEDIUM, direction: FontAwesomeAnimationSpinDirection = FontAwesomeAnimationSpinDirection.CLOCKWISE) -> None:
        super().__init__(icon = icon, file = file, size = size, color = color, background_color = background_color, speed = speed)
        self._animation_type = FontAwesomeAnimationType.BEAT
        self.__original_size = size
        self.__max_size = size + 4
        self.__current_size = size
        self.__increase_size = True
        self._cache_values()

    def animate(self) -> pygame.Surface:
        icon_surface = super().render(self._icon, self._color)
        self._tmp_surface = pygame.Surface(icon_surface.get_size())
        if (self.__increase_size):
            if self.__current_size < self.__max_size:
                self.__current_size += 1
            else:
                self.__increase_size = False
        else:
            if self.__current_size > self.__original_size:
                self.__current_size -= 1
            else:
                self.__increase_size = True
        self.set_size(self.__current_size)
        if self._surface and self._tmp_surface:
            self._tmp_surface.blit(icon_surface.copy(), (0, 0))

        return icon_surface

class FontAwesomeIconFadeEffect(FontAwesomeIconBaseEffect):
    def __init__(self, icon: FontAwesomeUnicodeIcons, file: str, size: int, color: tuple[int, int, int] = (255, 255, 255), background_color: tuple[int, int, int, int] = (0, 0, 0, 0), speed: FontAwesomeAnimationSpeed = FontAwesomeAnimationSpeed.MEDIUM, direction: FontAwesomeAnimationSpinDirection = FontAwesomeAnimationSpinDirection.CLOCKWISE) -> None:
        super().__init__(icon = icon, file = file, size = size, color = color, background_color = background_color, speed = speed)
        self._animation_type = FontAwesomeAnimationType.FADE
        self.__alpha = 0
        self.__fade_in = True
        self._cache_values()

    def animate(self) -> pygame.Surface:
        __icon_surface = super().render(self._icon, self._color)
        __fade_icon_surface = pygame.Surface(__icon_surface.get_size())
        __fade_icon_surface.blit(__icon_surface.copy(), (0, 0))
        #__fade_icon_surface.set_alpha(self.__alpha)
        if self.__fade_in:
            if self.__alpha < 255:
                self.__alpha += 1
            else:
                self.__fade_in = False
        else:
            if self.__alpha > 0:
                self.__alpha -= 1
            else:
                self.__fade_in = True
        if self.__surface and self.__tmp_surface:
            self.__tmp_surface.blit(__fade_icon_surface.copy(), (0, 0))
        return __fade_icon_surface

class FontAwesomeIconSpinEffect(FontAwesomeIconBaseEffect):
    def __init__(self, icon: FontAwesomeUnicodeIcons, file: str, size: int, color: tuple[int, int, int] = (255, 255, 255), background_color: tuple[int, int, int, int] = (0, 0, 0, 0), speed: FontAwesomeAnimationSpeed = FontAwesomeAnimationSpeed.MEDIUM, direction: FontAwesomeAnimationSpinDirection = FontAwesomeAnimationSpinDirection.CLOCKWISE) -> None:
        super().__init__(icon = icon, file = file, size = size, color = color, background_color = background_color, speed = speed)
        if direction == FontAwesomeAnimationSpinDirection.CLOCKWISE:
            self._animation_type = FontAwesomeAnimationType.SPIN_CLOCKWISE
            self.__angle = 0
        else:
            self._animation_type = FontAwesomeAnimationType.SPIN_COUNTERCLOCKWISE
            self.__angle = 360
        self.__radius = 0
        self.__direction = direction
        self._cache_values()

    def _cache_values(self) -> None:
        if self._use_sprite_cache:
            self.__sprite_count = 359
            raise ValueError("TODO")
        else:
            # TODO: cached SPRITES better than ?
            self.__icon_surface = super().render(self._icon, self._color)
            square_size = max(self.__icon_surface.get_size())
            if len(self._background_color) == 4:
                self.__square_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
            else:
                self.__square_surface = pygame.Surface((square_size, square_size))
            self.__center = (self.__icon_surface.get_width() / 2, self.__icon_surface.get_height() / 2)

    def animate(self) -> pygame.Surface:
        x = self.__center[0] + self.__radius * math.cos(math.radians(self.__angle))
        y = self.__center[1] + self.__radius * math.sin(math.radians(self.__angle))
        self.__square_surface.fill(self._background_color)
        rotated_icon = pygame.transform.rotate(self.__icon_surface, self.__angle)
        rotated_rect = rotated_icon.get_rect(center = (x, y))
        self.__square_surface.blit(rotated_icon, rotated_rect)
        if self.__direction == FontAwesomeAnimationSpinDirection.CLOCKWISE:
            self.__angle = self.__angle - self._speed
            if self.__angle <= 0:
                self.__angle = 360
        else:
            self.__angle = self.__angle + self._speed
            if self.__angle > 360:
                self.__angle = 0
        return self.__square_surface
