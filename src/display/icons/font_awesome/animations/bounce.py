from typing import Optional
import pygame
from ..icon_animated import IconAnimated as FontAwesomeIconBaseEffect
from ..icon_list import IconList as FontAwesomeIcons
from ..enums import AnimationType as FontAwesomeAnimationType, AnimationSpeed as FontAwesomeAnimationSpeed

class FontAwesomeIconBounceEffect(FontAwesomeIconBaseEffect):
    def __init__(self, parent_surface: pygame.Surface, icon: FontAwesomeIcons, font_path: Optional[str] = None, size: int = 16, color: tuple[int, int, int] = (255, 255, 255), speed: FontAwesomeAnimationSpeed = FontAwesomeAnimationSpeed.MEDIUM) -> None:
        super().__init__(parent_surface = parent_surface, icon = icon, font_path = font_path, size = size, color = color, speed = speed)
        self._animation_type = FontAwesomeAnimationType.BOUNCE
        self.__icon_surface = super().render(self._icon, self._color)
        total_height = self.__icon_surface.get_height() + (self.__icon_surface.get_height() // 2)
        self.__real_surface_size = (self.__icon_surface.get_width(), total_height)
        self.__min_y = 0
        self.__max_y = total_height - self.__icon_surface.get_height()
        self.__distance = self.__max_y
        self.__current_y = 0
        self.__last_y = 0
        self.__falling = True
        self._set_animation_total_frames(self.__distance * 8)

    def __animate(self) -> None:
        self._set_animation_duration()
        if self.__min_y < self.__max_y:
            if self.__falling:
                if self.__current_y < self.__max_y:
                    self.__current_y += self._frame_skip
                else:
                    self.__falling = False
                    self.__min_y += self._frame_skip
            else:
                if self.__current_y > self.__min_y:
                    self.__current_y -= self._frame_skip
                else:
                    self.__falling = True

    @property
    def __changed(self) -> bool:
        return self.__last_y != int(self.__current_y)

    def __update_changed_values(self) -> None:
        self.__last_y = int(self.__current_y)

    def render(self) -> pygame.Surface:
        self.__animate()
        if self.__changed:
            tmp_surface = pygame.Surface(self.__real_surface_size, pygame.SRCALPHA)
            tmp_surface.blit(self.__icon_surface, (0, self.__current_y))
            self.__update_changed_values()
            return tmp_surface
        else:
            return None
