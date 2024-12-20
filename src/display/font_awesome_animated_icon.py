from abc import abstractmethod
from enum import Enum
import math
import datetime
import pygame

from .font_awesome_unicode_icons import FontAwesomeUnicodeIcons
from .font_awesome_icon import FontAwesomeIcon
from ..utils.logger import Logger

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
    def __init__(self, surface: pygame.Surface, x: int, y: int, icon: FontAwesomeUnicodeIcons, file: str, size: int, color: tuple[int, int, int] = (255, 255, 255), background_color: tuple[int, int, int, int] = (0, 0, 0, 0), speed: FontAwesomeAnimationSpeed = FontAwesomeAnimationSpeed.MEDIUM, use_sprite_cache: bool = False) -> None:
        super().__init__(file = file, size = size, color = color)
        self._log = Logger()
        self._surface = surface
        self._tmp_surface = None
        self.__x = x
        self.__y = y
        self._icon = icon
        self._color = color
        self.__background_color = background_color
        self.__transparent = len(background_color) == 4
        self._speed = speed
        self._use_sprite_cache = use_sprite_cache
        self._animation_type = FontAwesomeAnimationType.NONE,
        self._last_animation_timestamp = datetime.datetime.now().timestamp()

    def _transparent(self) -> bool:
        return self.__transparent

    # TODO: REMOVE
    def _background_color(self):
        return self.__background_color

    def _animation_frame_changed(self) -> bool:
        render_required = False
        last_animation_timestamp = datetime.datetime.now().timestamp()
        timestamp_diff = datetime.datetime.now().timestamp() - self._last_animation_timestamp
        if self._speed == FontAwesomeAnimationSpeed.FAST:
            if timestamp_diff > 0.01:
                render_required = True
                self._last_animation_timestamp = last_animation_timestamp
        elif self._speed == FontAwesomeAnimationSpeed.MEDIUM:
            if timestamp_diff > 0.05:
                render_required = True
                self._last_animation_timestamp = last_animation_timestamp
        elif self._speed == FontAwesomeAnimationSpeed.SLOW:
            if timestamp_diff > 0.10:
                render_required = True
                self._last_animation_timestamp = last_animation_timestamp
        else:
            raise ValueError("Invalid animation speed.")

        return render_required

    def animate(self) -> bool:
        if self._tmp_surface is not None:
            self._animate()
            self._surface.blit(self._tmp_surface, (self.__x, self.__y))
            self._tmp_surface.fill(self.__background_color)
            return True
        else:
            self._log.warning("Temporal surface not set")
            return False

    def _animate(self) -> pygame.Surface:
        raise ValueError("_animate method not declared")

class FontAwesomeIconBeatEffect(FontAwesomeIconBaseEffect):
    def __init__(self, surface: pygame.Surface, x: int, y: int, icon: FontAwesomeUnicodeIcons, file: str, size: int, color: tuple[int, int, int] = (255, 255, 255), background_color: tuple[int, int, int, int] = (0, 0, 0, 0), speed: FontAwesomeAnimationSpeed = FontAwesomeAnimationSpeed.MEDIUM, use_sprite_cache: bool = False, max_size: int = 0) -> None:
        super().__init__(surface = surface, x = x, y = y, icon = icon, file = file, size = size, color = color, background_color = background_color, speed = speed)
        self._animation_type = FontAwesomeAnimationType.BEAT
        self.__original_size = size
        if (max_size <= size):
            raise ValueError(f"Invalid max_size value: {max_size}.")
        self.__max_size = max_size
        self.__current_size = size
        self.__increase_size = True
        # set surface size at max Beat width/height
        super().set_size(self.__max_size)
        icon_surface = super().render(self._icon, self._color)
        self._tmp_surface = pygame.Surface((icon_surface.get_width(), icon_surface.get_height()))
        # restore original (start) size
        super().set_size(self.__original_size)

    def _animate(self) -> None:
        if True:
            draw_new_frame = self._animation_frame_changed()
            animation_unit = 1
            icon_surface = super().render(self._icon, self._color)
            if (self.__increase_size):
                if self.__current_size < self.__max_size:
                    if draw_new_frame:
                        self.__current_size += animation_unit
                else:
                    self.__increase_size = False
            else:
                if self.__current_size > self.__original_size:
                    if draw_new_frame:
                        self.__current_size -= animation_unit
                else:
                    self.__increase_size = True
            super().set_size(self.__current_size)
            if self._surface and self._tmp_surface:
                x = (self._tmp_surface.get_width() - icon_surface.get_width()) // 2
                y = (self._tmp_surface.get_height() - icon_surface.get_height()) // 2
                self._tmp_surface.blit(icon_surface, (x, y))

"""
class FontAwesomeIconFadeEffect(FontAwesomeIconBaseEffect):
    def __init__(self, surface: pygame.Surface, x: int, y: int, icon: FontAwesomeUnicodeIcons, file: str, size: int, color: tuple[int, int, int] = (255, 255, 255), background_color: tuple[int, int, int, int] = (0, 0, 0, 0), speed: FontAwesomeAnimationSpeed = FontAwesomeAnimationSpeed.MEDIUM, use_sprite_cache: bool = False, direction: FontAwesomeAnimationSpinDirection = FontAwesomeAnimationSpinDirection.CLOCKWISE) -> None:
        super().__init__(surface = surface, x = x, y = y, icon = icon, file = file, size = size, color = color, background_color = background_color, speed = speed)
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
        if self._tmp_surface is not None:
            self._tmp_surface.blit(__fade_icon_surface, (0, 0))
        return __fade_icon_surface

class FontAwesomeIconSpinEffect(FontAwesomeIconBaseEffect):
    def __init__(self, surface: pygame.Surface, x: int, y: int, icon: FontAwesomeUnicodeIcons, file: str, size: int, color: tuple[int, int, int] = (255, 255, 255), background_color: tuple[int, int, int, int] = (0, 0, 0, 0), speed: FontAwesomeAnimationSpeed = FontAwesomeAnimationSpeed.MEDIUM, use_sprite_cache: bool = False, direction: FontAwesomeAnimationSpinDirection = FontAwesomeAnimationSpinDirection.CLOCKWISE) -> None:
        super().__init__(surface = surface, x = x, y = y, icon = icon, file = file, size = size, color = color, background_color = background_color, speed = speed)
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
            if self._transparent:
                self.__square_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
            else:
                self.__square_surface = pygame.Surface((square_size, square_size))
            self.__center = (self.__icon_surface.get_width() / 2, self.__icon_surface.get_height() / 2)

    def animate(self) -> pygame.Surface:
        x = self.__center[0] + self.__radius * math.cos(math.radians(self.__angle))
        y = self.__center[1] + self.__radius * math.sin(math.radians(self.__angle))
        # TODO
        # self.__square_surface.fill(self._background_color)
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

"""