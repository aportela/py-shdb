from typing import Optional
import pygame
from ..icon_animated import IconAnimated as FontAwesomeIconBaseEffect
from ..icon_list import IconList as FontAwesomeIcons
from ..enums import AnimationType as FontAwesomeAnimationType, AnimationSpeed as FontAwesomeAnimationSpeed, FlipAnimationAxis as FontAwesomeAnimationFlipAxis

class FontAwesomeIconFlipEffect(FontAwesomeIconBaseEffect):

    def __init__(self, parent_surface: pygame.Surface, x: int, y: int, icon: FontAwesomeIcons, font_file_path: Optional[str] = None, size: int = 16, color: tuple[int, int, int] = (255, 255, 255), background_color: tuple[int, int, int] = None, speed: FontAwesomeAnimationSpeed = FontAwesomeAnimationSpeed.MEDIUM, axis: FontAwesomeAnimationFlipAxis = FontAwesomeAnimationFlipAxis.HORIZONTAL) -> None:
        super().__init__(parent_surface = parent_surface, x = x, y = y, icon = icon, font_file_path = font_file_path, size = size, color = color, background_color = background_color, speed = speed)
        if axis == FontAwesomeAnimationFlipAxis.HORIZONTAL:
            self._animation_type = FontAwesomeAnimationType.HORIZONTAL_FLIP
        else:
            self._animation_type = FontAwesomeAnimationType.VERTICAL_FLIP
        self.__shrinking = True
        self.__flip = False
        self.__icon_surface = super().render(self._icon, self._color)
        self.__icon_surface_flipped = pygame.transform.flip(self.__icon_surface, self._animation_type == FontAwesomeAnimationType.HORIZONTAL_FLIP, self._animation_type == FontAwesomeAnimationType.VERTICAL_FLIP)
        self.__width_cache = self.__icon_surface.get_width()
        self.__current_width = self.__width_cache
        self.__height_cache = self.__icon_surface.get_height()
        self.__current_height = self.__height_cache
        if self._animation_type == FontAwesomeAnimationType.HORIZONTAL_FLIP:
            self._set_animation_total_frames(self.__width_cache * 4)
        else:
            self._set_animation_total_frames(self.__height_cache * 4)
        super()._create_temporal_surface((self.__width_cache, self.__height_cache))

    def _animate(self) -> bool:
        if True or self._animation_frame_change_required():
            streched_icon = pygame.transform.scale(self.__icon_surface if self.__flip else self.__icon_surface_flipped, (self.__current_width, self.__current_height))
            if self._animation_type == FontAwesomeAnimationType.HORIZONTAL_FLIP:
                dest = ((self.__width_cache - self.__current_width) // 2, 0)
            else:
                dest = (0, (self.__height_cache - self.__current_height) // 2)
            self._blit(streched_icon, dest)
            if self.__shrinking:
                if self._animation_type == FontAwesomeAnimationType.HORIZONTAL_FLIP:
                    self.__current_width -= self._frame_skip
                    if self.__current_width < 1:
                        self.__current_width = 1
                        self.__shrinking = False
                        self.__flip = not self.__flip
                else:
                    self.__current_height -= self._frame_skip
                    if self.__current_height < 1:
                        self.__current_height = 1
                        self.__shrinking = False
                        self.__flip = not self.__flip
            else:
                if self._animation_type == FontAwesomeAnimationType.HORIZONTAL_FLIP:
                    self.__current_width += self._frame_skip
                    if self.__current_width >= self.__width_cache:
                        self.__current_width = self.__width_cache
                        self.__shrinking = True
                else:
                    self.__current_height += self._frame_skip
                    if self.__current_height >= self.__height_cache:
                        self.__current_height = self.__height_cache
                        self.__shrinking = True
            return True
        else:
            return False