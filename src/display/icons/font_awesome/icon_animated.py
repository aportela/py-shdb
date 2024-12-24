from typing import Optional

import datetime
import pygame

from .icon_list import IconList as FontAwesomeIcons
from .icon import Icon as FontAwesomeIcon
from ....utils.logger import Logger
from ...fps import FPS

from .enums import AnimationType as FontAwesomeAnimationType, AnimationSpeed as FontAwesomeAnimationSpeed

class IconAnimated(FontAwesomeIcon):
    def __init__(self, parent_surface: pygame.Surface, x: int, y: int, icon: FontAwesomeIcons, font_file_path: Optional[str] = None, size: int = 16, color: tuple[int, int, int] = (255, 255, 255), background_color: tuple[int, int, int] = None, speed: FontAwesomeAnimationSpeed = FontAwesomeAnimationSpeed.MEDIUM, animation_duration_coefficients: tuple[int, int, int] = (1, 2, 4), animation_total_frames: int = 0) -> None:
        super().__init__(font_file_path = font_file_path, size = size, color = color)
        self._log = Logger()
        self._parent_surface = parent_surface
        self.__tmp_surface = None
        self.__x = x
        self.__y = y
        self._icon = icon
        self._color = color
        self.__background_color = background_color
        self.__transparent = background_color == None
        self._speed = speed
        self._set_animation_duration_coefficients(animation_duration_coefficients)
        self._sprite_count = 0
        self._animation_type = FontAwesomeAnimationType.NONE,
        self.__animation_total_frames = animation_total_frames
        self._last_animation_timestamp = datetime.datetime.now().timestamp()
        self.__widget_area = None
        self.__sub_surface = None

    def clear_prev(self) -> None:
        self._parent_surface.blit(self.__sub_surface, self.__widget_area)

    def update_1(self) -> None:
        pygame.display.update(self.__widget_area)

    def _transparent(self) -> bool:
        return self.__transparent

    def _create_temporal_surface(self, size: tuple [int, int]) -> None:
        if self._transparent:
            self.__tmp_surface = pygame.Surface(size, pygame.SRCALPHA)
        else:
            self.__tmp_surface = pygame.Surface(size)
        if self.__widget_area is None:
            self.__widget_area = pygame.Rect(self.__x, self.__y, size[0], size[1])
        if self.__sub_surface is None:
            self.__sub_surface = self._parent_surface.subsurface(self.__widget_area).copy()

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
        if self.__background_color is None:
            self.__tmp_surface.fill((0, 0, 0, 0))
        else:
            self.__tmp_surface.fill(self.__background_color)

    def _blit(self, surface: pygame.Surface, dest: tuple[int, int]) -> None:
        #self.__tmp_surface.fill(self.__background_color)
        self.__tmp_surface.blit(surface, dest)

    def animate(self) -> bool:
        if self._parent_surface is not None:
            self.__animation_duration = self.__set_animation_duration(FPS.get_current_fps(), self._speed)
            if self._animate():
                self._parent_surface.blit(self.__tmp_surface, (self.__x, self.__y))
                return True
            else:
                return False
        else:
            self._log.warning("Temporal surface not set.")
            return False

    def _animate(self) -> bool:
        raise ValueError("Missing _animate method.")

    def _set_animation_duration(self):
        self.__animation_duration = self.__set_animation_duration(FPS.get_current_fps(), self._speed)
