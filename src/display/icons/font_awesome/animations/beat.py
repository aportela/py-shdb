from typing import Optional
import pygame
from ..icon_animated import IconAnimated as FontAwesomeIconBaseEffect
from ..icon_list import IconList as FontAwesomeIcons
from ..enums import AnimationType as FontAwesomeAnimationType, AnimationSpeed as FontAwesomeAnimationSpeed

class FontAwesomeIconBeatEffect(FontAwesomeIconBaseEffect):
    def __init__(self, parent_surface: pygame.Surface, x: int, y: int, icon: FontAwesomeIcons, font_path: Optional[str] = None, size: int = 16, color: tuple[int, int, int] = (255, 255, 255), speed: FontAwesomeAnimationSpeed = FontAwesomeAnimationSpeed.MEDIUM, max_size: int = 0) -> None:
        super().__init__(parent_surface = parent_surface, x = x, y = y, icon = icon, font_path = font_path, size = size, color = color, speed = speed)
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
        self.__size = big_size_cached
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
        if self.__last_size != int(self.__current_size):
            super().set_size(int(self.__current_size))
            icon_surface = super().render(self._icon, self._color)
            x = (self._get_temporal_surface_width() - icon_surface.get_width()) // 2
            y = (self._get_temporal_surface_height() - icon_surface.get_height()) // 2
            self._blit(icon_surface, (x, y))
            self.__last_size = int(self.__current_size)
            return True
        else:
            return False

    def render(self) -> pygame.Surface:
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
        if self.__last_size != int(self.__current_size):
            tmp_surface = pygame.Surface(self.__size, pygame.SRCALPHA)
            super().set_size(int(self.__current_size))
            icon_surface = super().render(self._icon, self._color)
            x = (self._get_temporal_surface_width() - icon_surface.get_width()) // 2
            y = (self._get_temporal_surface_height() - icon_surface.get_height()) // 2
            tmp_surface.blit(icon_surface, (x, y))
            self.__last_size = int(self.__current_size)
            return tmp_surface
        else:
            return None

    #def reset_animation(self):
        # TODO
