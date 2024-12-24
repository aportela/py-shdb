from typing import Optional
import pygame

from .enums import AnimationType as FontAwesomeAnimationType, AnimationSpeed as FontAwesomeAnimationSpeed
from .icon_list import IconList as FontAwesomeIcon
from .icon import Icon
from ...fps import FPS

class IconAnimated(Icon):
    def __init__(self, parent_surface: pygame.Surface, icon: FontAwesomeIcon, font_path: Optional[str] = None, size: int = 16, color: tuple[int, int, int] = (255, 255, 255), speed: FontAwesomeAnimationSpeed = FontAwesomeAnimationSpeed.MEDIUM, speed_durations: tuple[int, int, int] = (1, 2, 4), total_frames: int = 0) -> None:
        super().__init__(font_path = font_path, size = size, color = color)
        self._animation_type = FontAwesomeAnimationType.NONE,
        self._parent_surface = parent_surface
        self._icon = icon
        self._color = color
        self._speed = speed
        self.__set_speed_durations(speed_durations)
        self.__total_frames = total_frames

    def _set_total_frames(self, total_frames: int) -> None:
        self.__total_frames = total_frames

    def __set_speed_durations(self, animation_duration_coefficients: tuple[int, int, int] = (1, 2, 4)) -> None:
        self.__animation_duration_coefficients = animation_duration_coefficients
        self.__animation_duration = 0

    @property
    def _frame_skip(self) -> float:
        if self.__animation_duration > 0:
            return self.__total_frames / self.__animation_duration
        else:
            return 0

    def __update_animation_duration(self):
        if self._speed == FontAwesomeAnimationSpeed.FAST:
            self.__animation_duration = FPS.get_current_fps() * self.__animation_duration_coefficients[0]
        elif self._speed == FontAwesomeAnimationSpeed.MEDIUM:
            self.__animation_duration = FPS.get_current_fps() * self.__animation_duration_coefficients[1]
        elif self._speed == FontAwesomeAnimationSpeed.SLOW:
            self.__animation_duration = FPS.get_current_fps() * self.__animation_duration_coefficients[2]
        else:
            raise ValueError("Invalid FontAwesome animation speed value.")


    def _animate(self) -> None:
        raise ValueError(f"You must override this method (_animate) in this inherited class.")

    def __animate(self) -> None:
        self.__update_animation_duration()
        self._animate()

    @property
    def _changed(self) -> bool:
        raise ValueError(f"You must override this property (_changed) in this inherited class.")

    def _update_changed_values(self) -> None:
        raise ValueError(f"You must override this method (_update_changed_values) in this inherited class.")

    def _render_animation(self) -> pygame.Surface:
        raise ValueError(f"You must override this method (_render_animation) in this inherited class.")

    def render_animation(self) -> pygame.Surface:
        self.__animate()
        if self._changed:
            surface = self._render_animation()
            self._update_changed_values()
            return surface
        else:
            return None