from typing import Optional
import pygame

from ..animated_icon import FontAwesomeIconBaseEffect
from ..icon_list import IconList as FontAwesomeIcons
from ..enums import AnimationType as FontAwesomeAnimationType, AnimationSpeed as FontAwesomeAnimationSpeed

class FontAwesomeIconBeatAndFadeEffect(FontAwesomeIconBaseEffect):
    def __init__(self, parent_surface: pygame.Surface, x: int, y: int, icon: FontAwesomeIcons, font_file_path: Optional[str] = None, size: int = 16, color: tuple[int, int, int] = (255, 255, 255), background_color: tuple[int, int, int] = None, speed: FontAwesomeAnimationSpeed = FontAwesomeAnimationSpeed.MEDIUM, max_size: int = 0) -> None:
        super().__init__(parent_surface = parent_surface, x = x, y = y, icon = icon, font_file_path = font_file_path, size = size, color = color, background_color = background_color, speed = speed)
        self._animation_type = FontAwesomeAnimationType.BEAT_AND_FADE
        self.__original_size = size
        if (max_size <= size):
            raise ValueError(f"Invalid max_size value: {max_size}.")
        self.__max_size = max_size
        self.__current_size = size
        self.__increase_size = True
        self.__alpha = 72
        # set temporal font size at max Beat width/height for creating temporal surface with required size
        super().set_size(self.__max_size)
        icon_surface = super().render(self._icon, self._color)
        super()._create_temporal_surface(icon_surface.get_size())
        # restore original size
        super().set_size(self.__original_size)

    def _animate(self) -> bool:
        # TODO
        if self._animation_frame_change_required():
            animation_unit = 1
            icon_surface = super().render(self._icon, self._color)
            icon_surface.set_alpha(self.__alpha)
            if self.__increase_size:
                if self.__current_size < self.__max_size:
                    self.__current_size += animation_unit
                    if self.__alpha < 255:
                        self.__alpha += animation_unit * 16
                else:
                    self.__increase_size = False
            else:
                if self.__current_size > self.__original_size:
                    self.__current_size -= animation_unit
                    if self.__alpha > 72:
                        self.__alpha -= animation_unit * 16
                else:
                    self.__increase_size = True
            super().set_size(self.__current_size)
            x = (self._get_temporal_surface_width() - icon_surface.get_width()) // 2
            y = (self._get_temporal_surface_height() - icon_surface.get_height()) // 2
            self._blit(icon_surface, (x, y))
            return True
        else:
            return False
