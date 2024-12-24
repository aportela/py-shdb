from typing import Optional
import pygame
from ..icon_animated import IconAnimated as FontAwesomeIconBaseEffect
from ..icon_list import IconList as FontAwesomeIcons
from ..enums import AnimationType as FontAwesomeAnimationType, AnimationSpeed as FontAwesomeAnimationSpeed

class FontAwesomeIconBeatEffect(FontAwesomeIconBaseEffect):
    def __init__(self, parent_surface: pygame.Surface, icon: FontAwesomeIcons, font_path: Optional[str] = None, size: int = 16, color: tuple[int, int, int] = (255, 255, 255), speed: FontAwesomeAnimationSpeed = FontAwesomeAnimationSpeed.MEDIUM, max_size: int = 0) -> None:
        super().__init__(parent_surface = parent_surface, icon = icon, font_path = font_path, size = size, color = color, speed = speed)
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
        self.__real_surface_size = big_size_cached
        # restore original size
        super().set_size(self.__original_size)
        icon_surface = super().render(self._icon, self._color)
        small_size_cached = icon_surface.get_size()
        self._set_animation_total_frames((max(big_size_cached) - max(small_size_cached)) * 4)

    def __animate(self) -> None:
        self._set_animation_duration()
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

    @property
    def __changed(self) -> bool:
        return self.__last_size != int(self.__current_size)

    def __update_changed_values(self) -> None:
        self.__last_size = int(self.__current_size)

    def render(self) -> pygame.Surface:
        self._set_animation_duration()
        self.__animate()
        if self.__changed:
            tmp_surface = pygame.Surface(self.__real_surface_size, pygame.SRCALPHA)
            super().set_size(int(self.__current_size))
            icon_surface = super().render(self._icon, self._color)
            x = (self.__real_surface_size[0] - icon_surface.get_width()) // 2
            y = (self.__real_surface_size[1] - icon_surface.get_height()) // 2
            tmp_surface.blit(icon_surface, (x, y))
            self.__update_changed_values()
            return tmp_surface
        else:
            return None
