from typing import Optional
import math
import pygame
from ..icon_animated import IconAnimated as FontAwesomeIconBaseEffect
from ..icon_list import IconList as FontAwesomeIcons
from ..enums import AnimationType as FontAwesomeAnimationType, AnimationSpeed as FontAwesomeAnimationSpeed, SpinAnimationDirection as FontAwesomeAnimationSpinDirection

class FontAwesomeIconSpinEffect(FontAwesomeIconBaseEffect):
    def __init__(self, parent_surface: pygame.Surface, x: int, y: int, icon: FontAwesomeIcons, font_file_path: Optional[str] = None, size: int = 16, color: tuple[int, int, int] = (255, 255, 255), background_color: tuple[int, int, int] = None, speed: FontAwesomeAnimationSpeed = FontAwesomeAnimationSpeed.MEDIUM, animation_duration_coefficients: tuple[int, int, int] = (1, 2, 4), direction: FontAwesomeAnimationSpinDirection = FontAwesomeAnimationSpinDirection.CLOCKWISE) -> None:
        super().__init__(parent_surface = parent_surface, x = x, y = y, icon = icon, font_file_path = font_file_path, size = size, color = color, background_color = background_color, speed = speed, animation_duration_coefficients = animation_duration_coefficients, animation_total_frames = 359)
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
