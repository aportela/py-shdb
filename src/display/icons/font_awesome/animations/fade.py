from typing import Optional
import pygame
from ..icon_animated import IconAnimated as FontAwesomeIconBaseEffect
from ..icon_list import IconList as FontAwesomeIcons
from ..enums import AnimationType as FontAwesomeAnimationType, AnimationSpeed as FontAwesomeAnimationSpeed

class FontAwesomeIconFadeEffect(FontAwesomeIconBaseEffect):
    def __init__(self, parent_surface: pygame.Surface, x: int, y: int, icon: FontAwesomeIcons, font_file_path: Optional[str] = None, size: int = 16, color: tuple[int, int, int] = (255, 255, 255), background_color: tuple[int, int, int] = None, speed: FontAwesomeAnimationSpeed = FontAwesomeAnimationSpeed.MEDIUM, direction: FontAwesomeAnimationSpinDirection = FontAwesomeAnimationSpinDirection.CLOCKWISE) -> None:
        super().__init__(parent_surface = parent_surface, x = x, y = y, icon = icon, font_file_path = font_file_path, size = size, color = color, background_color = background_color, speed = speed)
        self._animation_type = FontAwesomeAnimationType.FADE
        self.__current_alpha = 0
        self.__last_alpha = 0
        self.__min_alpha = self.__current_alpha
        self.__max_alpha = 255
        self._set_animation_total_frames((self.__max_alpha - self.__min_alpha) * 4)
        self.__fade_in = True
        self.__icon_surface = super().render(self._icon, self._color)
        super()._create_temporal_surface(self.__icon_surface.get_size())

    def _animate(self) -> bool:
        if self.__fade_in:
            if self.__current_alpha < self.__max_alpha:
                self.__current_alpha += self._frame_skip
            else:
                self.__fade_in = False
        else:
            if self.__current_alpha > self.__min_alpha:
                self.__current_alpha -= self._frame_skip
            else:
                self.__fade_in = True

        if (self.__last_alpha != int(self.__current_alpha)):
            self.__icon_surface.set_alpha(int(self.__current_alpha))
            self._blit(self.__icon_surface, (0, 0))
            self.__last_alpha = int(self.__current_alpha)
            return True
        else:
            return False
