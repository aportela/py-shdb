from typing import Optional
import pygame
from ..icon_animated import IconAnimated as FontAwesomeIconBaseEffect
from ..icon_list import IconList as FontAwesomeIcons
from ..enums import AnimationType as FontAwesomeAnimationType, AnimationSpeed as FontAwesomeAnimationSpeed, SpinAnimationDirection as FontAwesomeAnimationSpinDirection

class FontAwesomeIconSpinEffect(FontAwesomeIconBaseEffect):
    def __init__(self, parent_surface: pygame.Surface, icon: FontAwesomeIcons, font_path: Optional[str] = None, size: int = 16, color: tuple[int, int, int] = (255, 255, 255), speed: FontAwesomeAnimationSpeed = FontAwesomeAnimationSpeed.MEDIUM, animation_duration_coefficients: tuple[int, int, int] = (1, 2, 4), direction: FontAwesomeAnimationSpinDirection = FontAwesomeAnimationSpinDirection.CLOCKWISE) -> None:
        super().__init__(parent_surface = parent_surface, icon = icon, font_path = font_path, size = size, color = color, speed = speed, animation_duration_coefficients = animation_duration_coefficients, animation_total_frames = 359)
        if direction == FontAwesomeAnimationSpinDirection.CLOCKWISE:
            self._animation_type = FontAwesomeAnimationType.SPIN_CLOCKWISE
            self.__angle = 0
        else:
            self._animation_type = FontAwesomeAnimationType.SPIN_COUNTERCLOCKWISE
            self.__angle = 360
        self.__last_angle = self.__angle
        self.__radius = 0
        self.__icon_surface = super().render(self._icon, self._color)
        self.__real_surface_size = self.__icon_surface.get_size()
        #square_size = max(self.__icon_surface.get_size())
        #super()._create_temporal_surface((square_size, square_size))
        self.__icon_surface_center = (self.__icon_surface.get_width() // 2, self.__icon_surface.get_height() // 2)


    def __animate(self) -> None:
        self._set_animation_duration()
        if self._animation_type == FontAwesomeAnimationType.SPIN_CLOCKWISE:
            self.__angle -= self._frame_skip
            if self.__angle <= 0:
                self.__angle = 360
        else:
            self.__angle += self._frame_skip
            if self.__angle > 360:
                self.__angle = 0

    def __changed(self) -> bool:
        return self.__last_angle != int(self.__angle)

    def render(self) -> bool:
        self.__animate()
        if self.__changed:
            tmp_surface = pygame.Surface(self.__real_surface_size, pygame.SRCALPHA)
            rotated_icon = pygame.transform.rotate(self.__icon_surface, self.__angle)
            rotated_rect = rotated_icon.get_rect(center = self.__icon_surface_center)
            tmp_surface.blit(rotated_icon, rotated_rect)
            self.__last_angle = int(self.__angle)
            return tmp_surface
        else:
            return None
