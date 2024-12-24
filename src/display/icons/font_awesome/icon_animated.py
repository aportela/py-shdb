from typing import Optional
import pygame

from .enums import AnimationType as FontAwesomeAnimationType, AnimationSpeed as FontAwesomeAnimationSpeed
from .icon_list import IconList as FontAwesomeIcon
from .icon import Icon
from ...fps import FPS

class IconAnimated(Icon):
    def __init__(self, parent_surface: pygame.Surface, icon: FontAwesomeIcon, font_path: Optional[str] = None, size: int = 16, color: tuple[int, int, int] = (255, 255, 255), speed: FontAwesomeAnimationSpeed = FontAwesomeAnimationSpeed.MEDIUM, animation_duration_coefficients: tuple[int, int, int] = (1, 2, 4), animation_total_frames: int = 0) -> None:
        super().__init__(font_path = font_path, size = size, color = color)
        self._animation_type = FontAwesomeAnimationType.NONE,
        self._parent_surface = parent_surface
        self._icon = icon
        self._color = color
        self._speed = speed
        self._set_animation_duration_coefficients(animation_duration_coefficients)
        self.__animation_total_frames = animation_total_frames

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
            raise ValueError("Invalid FontAwesome animation speed value.")

    @property
    def _frame_skip(self) -> float:
        if self.__animation_duration > 0:
            return self.__animation_total_frames / self.__animation_duration
        else:
            return 0

    def _set_animation_duration(self):
        self.__animation_duration = self.__set_animation_duration(FPS.get_current_fps(), self._speed)
