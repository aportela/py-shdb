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
    HORIZONTAL = 1
    VERTICAL = 2

class FontAwesomeAnimationSpinDirection(Enum):
    CLOCKWISE = 1
    COUNTERCLOCKWISE = 2

class FontAwesomeIconBaseEffect(FontAwesomeIcon):
    def __init__(self, surface: pygame.Surface, x: int, y: int, icon: FontAwesomeUnicodeIcons, file: str, size: int, color: tuple[int, int, int] = (255, 255, 255), background_color: tuple[int, int, int, int] = (0, 0, 0, 0), speed: FontAwesomeAnimationSpeed = FontAwesomeAnimationSpeed.MEDIUM, animation_duration_coefficients: tuple[int, int, int] = (1, 2, 4), animation_total_frames: int = 0, use_sprite_cache: bool = False) -> None:
        super().__init__(file = file, size = size, color = color)
        self._log = Logger()
        self._surface = surface
        self.__tmp_surface = None
        self.__x = x
        self.__y = y
        self._icon = icon
        self._color = color
        self.__background_color = background_color
        self.__transparent = len(background_color) == 4
        self._speed = speed
        self._set_animation_duration_coefficients(animation_duration_coefficients)
        if use_sprite_cache:
            raise ValueError("TODO")
        self._use_sprite_cache = use_sprite_cache
        self._sprite_count = 0
        self._animation_type = FontAwesomeAnimationType.NONE,
        self.__animation_total_frames = animation_total_frames
        self._last_animation_timestamp = datetime.datetime.now().timestamp()

    def _transparent(self) -> bool:
        return self.__transparent

    def _create_temporal_surface(self, size: tuple [int, int]) -> None:
        if self._transparent:
            self.__tmp_surface = pygame.Surface(size, pygame.SRCALPHA)
        else:
            self.__tmp_surface = pygame.Surface(size)

    def _get_temporal_surface_width(self) -> int:
        if self.__tmp_surface is not None:
            return self.__tmp_surface.get_width()
        else:
            return 0

    def _get_temporal_surface_height(self) -> int:
        if self.__tmp_surface is not None:
            return self.__tmp_surface.get_height()
        else:
            return 0

    def _set_animation_total_frames(self, total_frames: int) -> None:
        self.__animation_total_frames = total_frames

    def _set_animation_duration_coefficients(self, animation_duration_coefficients: tuple[int, int, int] = (1, 2, 4)) -> None:
        self.__animation_duration_coefficients = animation_duration_coefficients
        self.__animation_duration = 0

    def __set_animation_duration(self, current_fps: int, speed: FontAwesomeAnimationSpeed) -> None:
        if speed == FontAwesomeAnimationSpeed.FAST:
            return current_fps * self.__animation_duration_coefficients[0]
        elif speed == FontAwesomeAnimationSpeed.MEDIUM:
            return current_fps * self.__animation_duration_coefficients[1]
        elif speed == FontAwesomeAnimationSpeed.SLOW:
            return current_fps * self.__animation_duration_coefficients[2]
        else:
            raise ValueError("")

    @property
    def _frame_skip(self) -> float:
        if self.__animation_duration > 0:
            return self.__animation_total_frames / self.__animation_duration
        else:
            return 0

    def _create_tmp_surface(self, size: tuple[int, int]) -> None:
        raise ValueError("TODO.")

    def _animation_frame_change_required(self) -> bool:
        # TODO: use _total_frames && _skip_frames to fill animation_unit
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

    def _clear(self) -> None:
        self.__tmp_surface.fill(self.__background_color)

    def _blit(self, surface: pygame.Surface, dest: tuple[int, int]) -> None:
        self.__tmp_surface.fill(self.__background_color)
        self.__tmp_surface.blit(surface, dest)

    def animate(self, current_fps: int) -> bool:
        if self.__tmp_surface is not None:
            self.__animation_duration = self.__set_animation_duration(current_fps, self._speed)
            if self._animate():
                self._surface.blit(self.__tmp_surface, (self.__x, self.__y))
                return True
            else:
                return False
        else:
            self._log.warning("Temporal surface not set.")
            return False

    def _animate(self) -> bool:
        raise ValueError("Missing _animate method.")

class FontAwesomeIconBeatEffect(FontAwesomeIconBaseEffect):
    def __init__(self, surface: pygame.Surface, x: int, y: int, icon: FontAwesomeUnicodeIcons, file: str, size: int, color: tuple[int, int, int] = (255, 255, 255), background_color: tuple[int, int, int, int] = (0, 0, 0, 0), speed: FontAwesomeAnimationSpeed = FontAwesomeAnimationSpeed.MEDIUM, use_sprite_cache: bool = False, max_size: int = 0) -> None:
        super().__init__(surface = surface, x = x, y = y, icon = icon, file = file, size = size, color = color, background_color = background_color, speed = speed)
        self._animation_type = FontAwesomeAnimationType.BEAT
        self.__original_size = size
        if (max_size <= size):
            raise ValueError(f"Invalid max_size value: {max_size}.")
        self.__max_size = max_size
        self.__current_size = size
        self.__last_size = 0
        self.__increase_size = True
        # set temporal font size at max Beat width/height for creating temporal surface with required size
        super().set_size(self.__max_size)
        icon_surface = super().render(self._icon, self._color)
        big_size_cached = icon_surface.get_size()
        super()._create_temporal_surface(big_size_cached)
        # restore original size
        super().set_size(self.__original_size)
        icon_surface = super().render(self._icon, self._color)
        small_size_cached = icon_surface.get_size()
        self._set_animation_total_frames((max(big_size_cached) - max(small_size_cached)) * 4)

    def _animate(self) -> bool:
        if self.__increase_size:
            if self.__current_size < self.__max_size:
                self.__current_size += self._frame_skip
            else:
                self.__increase_size = False
        else:
            if self.__current_size > self.__original_size:
                self.__current_size -= self._frame_skip
            else:
                self.__increase_size = True
        super().set_size(int(self.__current_size))
        if self.__last_size != self.__current_size:
            icon_surface = super().render(self._icon, self._color)
            x = (self._get_temporal_surface_width() - icon_surface.get_width()) // 2
            y = (self._get_temporal_surface_height() - icon_surface.get_height()) // 2
            self._blit(icon_surface, (x, y))
            self.__last_size = self.__current_size
            return True
        else:
            return False

class FontAwesomeIconBeatAndFadeEffect(FontAwesomeIconBaseEffect):
    def __init__(self, surface: pygame.Surface, x: int, y: int, icon: FontAwesomeUnicodeIcons, file: str, size: int, color: tuple[int, int, int] = (255, 255, 255), background_color: tuple[int, int, int, int] = (0, 0, 0, 0), speed: FontAwesomeAnimationSpeed = FontAwesomeAnimationSpeed.MEDIUM, use_sprite_cache: bool = False, max_size: int = 0) -> None:
        super().__init__(surface = surface, x = x, y = y, icon = icon, file = file, size = size, color = color, background_color = background_color, speed = speed)
        self._animation_type = FontAwesomeAnimationType.BEAT_AND_FADE
        self.__original_size = size
        if (max_size <= size):
            raise ValueError(f"Invalid max_size value: {max_size}.")
        self.__max_size = max_size
        self.__current_size = size
        self.__increase_size = True
        self.__alpha = 72
        # set temporal font size at max Beat width/height for creating temporal surface with required size
        super().set_size(self.__max_size)
        icon_surface = super().render(self._icon, self._color)
        super()._create_temporal_surface(icon_surface.get_size())
        # restore original size
        super().set_size(self.__original_size)

    def _animate(self) -> bool:
        if self._animation_frame_change_required():
            animation_unit = 1
            icon_surface = super().render(self._icon, self._color)
            icon_surface.set_alpha(self.__alpha)
            if self.__increase_size:
                if self.__current_size < self.__max_size:
                    self.__current_size += animation_unit
                    if self.__alpha < 255:
                        self.__alpha += animation_unit * 16
                else:
                    self.__increase_size = False
            else:
                if self.__current_size > self.__original_size:
                    self.__current_size -= animation_unit
                    if self.__alpha > 72:
                        self.__alpha -= animation_unit * 16
                else:
                    self.__increase_size = True
            super().set_size(self.__current_size)
            x = (self._get_temporal_surface_width() - icon_surface.get_width()) // 2
            y = (self._get_temporal_surface_height() - icon_surface.get_height()) // 2
            self._blit(icon_surface, (x, y))
            return True
        else:
            return False

class FontAwesomeIconBounceEffect(FontAwesomeIconBaseEffect):
    def __init__(self, surface: pygame.Surface, x: int, y: int, icon: FontAwesomeUnicodeIcons, file: str, size: int, color: tuple[int, int, int] = (255, 255, 255), background_color: tuple[int, int, int, int] = (0, 0, 0, 0), speed: FontAwesomeAnimationSpeed = FontAwesomeAnimationSpeed.MEDIUM, use_sprite_cache: bool = False) -> None:
        super().__init__(surface = surface, x = x, y = y, icon = icon, file = file, size = size, color = color, background_color = background_color, speed = speed)
        self._animation_type = FontAwesomeAnimationType.BOUNCE
        self.__icon_surface = super().render(self._icon, self._color)
        total_height = self.__icon_surface.get_height() + (self.__icon_surface.get_height() // 2)
        super()._create_temporal_surface((self.__icon_surface.get_width(), total_height))
        self.__x = 0
        self.__y = 0
        self.__min_y = 0
        self.__max_y = total_height - self.__icon_surface.get_height()
        self.__falling = True
        self.__animation_unit = 2

    def _animate(self) -> bool:
        if self._animation_frame_change_required():
            if self.__min_y < self.__max_y:
                if self.__falling:
                    if self.__y < self.__max_y:
                        self.__y += self.__animation_unit
                    else:
                        self.__falling = False
                        self.__min_y += self.__animation_unit
                        #self.__animation_unit += 1
                else:
                    if self.__y > self.__min_y:
                        self.__y -= self.__animation_unit
                    else:
                        self.__falling = True
                self._blit(self.__icon_surface, (self.__x, self.__y))
                return True
            else:
                return False
        else:
            return False

class FontAwesomeIconFadeEffect(FontAwesomeIconBaseEffect):
    def __init__(self, surface: pygame.Surface, x: int, y: int, icon: FontAwesomeUnicodeIcons, file: str, size: int, color: tuple[int, int, int] = (255, 255, 255), background_color: tuple[int, int, int, int] = (0, 0, 0, 0), speed: FontAwesomeAnimationSpeed = FontAwesomeAnimationSpeed.MEDIUM, use_sprite_cache: bool = False, direction: FontAwesomeAnimationSpinDirection = FontAwesomeAnimationSpinDirection.CLOCKWISE) -> None:
        super().__init__(surface = surface, x = x, y = y, icon = icon, file = file, size = size, color = color, background_color = background_color, speed = speed)
        self._animation_type = FontAwesomeAnimationType.FADE
        self.__current_alpha = 0
        self.__min_alpha = self.__current_alpha
        self.__max_alpha = 255
        self._set_animation_total_frames(self.__max_alpha - self.__min_alpha)
        self.__fade_in = True
        self.__icon_surface = super().render(self._icon, self._color)
        super()._create_temporal_surface(self.__icon_surface.get_size())

    def _animate(self) -> bool:
        if True or self._animation_frame_change_required():
            self.__icon_surface.set_alpha(self.__current_alpha)
            self._blit(self.__icon_surface, (0, 0))
            animation_unit = 10
            if self.__fade_in:
                if self.__current_alpha < self.__max_alpha:
                    self.__current_alpha += animation_unit
                else:
                    self.__fade_in = False
            else:
                if self.__current_alpha > self.__min_alpha:
                    self.__current_alpha -= animation_unit
                else:
                    self.__fade_in = True
            return True
        else:
            return False

class FontAwesomeIconSpinEffect(FontAwesomeIconBaseEffect):
    def __init__(self, surface: pygame.Surface, x: int, y: int, icon: FontAwesomeUnicodeIcons, file: str, size: int, color: tuple[int, int, int] = (255, 255, 255), background_color: tuple[int, int, int, int] = (0, 0, 0, 0), speed: FontAwesomeAnimationSpeed = FontAwesomeAnimationSpeed.MEDIUM, animation_duration_coefficients: tuple[int, int, int] = (1, 2, 4), use_sprite_cache: bool = False, direction: FontAwesomeAnimationSpinDirection = FontAwesomeAnimationSpinDirection.CLOCKWISE) -> None:
        super().__init__(surface = surface, x = x, y = y, icon = icon, file = file, size = size, color = color, background_color = background_color, speed = speed, animation_duration_coefficients = animation_duration_coefficients, animation_total_frames = 359)
        if direction == FontAwesomeAnimationSpinDirection.CLOCKWISE:
            self._animation_type = FontAwesomeAnimationType.SPIN_CLOCKWISE
            self.__angle = 0
        else:
            self._animation_type = FontAwesomeAnimationType.SPIN_COUNTERCLOCKWISE
            self.__angle = 360
        self.__last_angle = self.__angle
        self.__radius = 0
        self.__icon_surface = super().render(self._icon, self._color)
        square_size = max(self.__icon_surface.get_size())
        super()._create_temporal_surface((square_size, square_size))
        self.__icon_surface_center_cache = (self.__icon_surface.get_width() // 2, self.__icon_surface.get_height() // 2)
        self.__refresh_required = True

    def _animate(self) -> bool:
        if self.__refresh_required:
            x = self.__icon_surface_center_cache[0] + self.__radius * math.cos(math.radians(self.__angle))
            y = self.__icon_surface_center_cache[1] + self.__radius * math.sin(math.radians(self.__angle))
            rotated_icon = pygame.transform.rotate(self.__icon_surface, self.__angle)
            rotated_rect = rotated_icon.get_rect(center = (x, y))
            self._blit(rotated_icon, rotated_rect)
            self.__last_angle = int(self.__angle)
            if self._animation_type == FontAwesomeAnimationType.SPIN_CLOCKWISE:
                self.__angle -= self._frame_skip
                if self.__angle <= 0:
                    self.__angle = 360
            else:
                self.__angle += self._frame_skip
                if self.__angle > 360:
                    self.__angle = 0
            return self.__last_angle != int(self.__angle)
        else:
            return False

class FontAwesomeIconFlipEffect(FontAwesomeIconBaseEffect):
    def __init__(self, surface: pygame.Surface, x: int, y: int, icon: FontAwesomeUnicodeIcons, file: str, size: int, color: tuple[int, int, int] = (255, 255, 255), background_color: tuple[int, int, int, int] = (0, 0, 0, 0), speed: FontAwesomeAnimationSpeed = FontAwesomeAnimationSpeed.MEDIUM, use_sprite_cache: bool = False, axis: FontAwesomeAnimationFlipAxis = FontAwesomeAnimationFlipAxis.HORIZONTAL) -> None:
        super().__init__(surface = surface, x = x, y = y, icon = icon, file = file, size = size, color = color, background_color = background_color, speed = speed)
        if axis == FontAwesomeAnimationFlipAxis.HORIZONTAL:
            self._animation_type = FontAwesomeAnimationType.HORIZONTAL_FLIP
        else:
            self._animation_type = FontAwesomeAnimationType.VERTICAL_FLIP
        self.__shrinking = True
        self.__flip = False
        self.__icon_surface = super().render(self._icon, self._color)
        self.__icon_surface_flipped = pygame.transform.flip(self.__icon_surface, self._animation_type == FontAwesomeAnimationType.HORIZONTAL_FLIP, self._animation_type == FontAwesomeAnimationType.VERTICAL_FLIP)
        self.__width_cache = self.__icon_surface.get_width()
        self.__current_width = self.__width_cache
        self.__height_cache = self.__icon_surface.get_height()
        self.__current_height = self.__height_cache
        if self._animation_type == FontAwesomeAnimationType.HORIZONTAL_FLIP:
            self._set_animation_total_frames(self.__width_cache * 4)
        else:
            self._set_animation_total_frames(self.__height_cache * 4)
        super()._create_temporal_surface((self.__width_cache, self.__height_cache))

    def _animate(self) -> bool:
        if True or self._animation_frame_change_required():
            streched_icon = pygame.transform.scale(self.__icon_surface if self.__flip else self.__icon_surface_flipped, (self.__current_width, self.__current_height))
            if self._animation_type == FontAwesomeAnimationType.HORIZONTAL_FLIP:
                dest = ((self.__width_cache - self.__current_width) // 2, 0)
            else:
                dest = (0, (self.__height_cache - self.__current_height) // 2)
            self._blit(streched_icon, dest)
            if self.__shrinking:
                if self._animation_type == FontAwesomeAnimationType.HORIZONTAL_FLIP:
                    self.__current_width -= self._frame_skip
                    if self.__current_width < 1:
                        self.__current_width = 1
                        self.__shrinking = False
                        self.__flip = not self.__flip
                else:
                    self.__current_height -= self._frame_skip
                    if self.__current_height < 1:
                        self.__current_height = 1
                        self.__shrinking = False
                        self.__flip = not self.__flip
            else:
                if self._animation_type == FontAwesomeAnimationType.HORIZONTAL_FLIP:
                    self.__current_width += self._frame_skip
                    if self.__current_width >= self.__width_cache:
                        self.__current_width = self.__width_cache
                        self.__shrinking = True
                else:
                    self.__current_height += self._frame_skip
                    if self.__current_height >= self.__height_cache:
                        self.__current_height = self.__height_cache
                        self.__shrinking = True
            return True
        else:
            return False