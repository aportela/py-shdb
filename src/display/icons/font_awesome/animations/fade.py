from typing import Optional
import pygame
from ..icon_animated import IconAnimated as FontAwesomeIconBaseEffect
from ..icon_list import IconList as FontAwesomeIcons
from ..enums import AnimationType as FontAwesomeAnimationType, AnimationSpeed as FontAwesomeAnimationSpeed

class FontAwesomeIconFadeEffect(FontAwesomeIconBaseEffect):
    def __init__(self, parent_surface: pygame.Surface, icon: FontAwesomeIcons, font_path: Optional[str] = None, size: int = 16, color: tuple[int, int, int] = (255, 255, 255), speed: FontAwesomeAnimationSpeed = FontAwesomeAnimationSpeed.MEDIUM) -> None:
        super().__init__(parent_surface = parent_surface, icon = icon, font_path = font_path, size = size, color = color, speed = speed)
        self._animation_type = FontAwesomeAnimationType.FADE
        self.__min_alpha = 0
        self.__max_alpha = 255
        self.__current_alpha = self.__min_alpha
        self.__last_alpha = 0
        self.__fade_in = True
        self.__icon_surface = super().render(self._icon, self._color)
        self._set_animation_total_frames((self.__max_alpha - self.__min_alpha) * 4)

    def render(self) -> pygame.Surface:
        self._set_animation_duration()
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
        if self.__last_alpha != int(self.__current_alpha):
            self.__icon_surface.set_alpha(int(self.__current_alpha))
            self.__last_alpha = int(self.__current_alpha)
            return self.__icon_surface
        else:
            return None
