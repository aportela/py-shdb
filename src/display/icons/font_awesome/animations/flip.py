from typing import Optional
import pygame
from ..icon_animated import IconAnimated as FontAwesomeIconBaseEffect
from ..icon_list import IconList as FontAwesomeIcons
from ..enums import AnimationType as FontAwesomeAnimationType, AnimationSpeed as FontAwesomeAnimationSpeed, FlipAnimationAxis as FontAwesomeAnimationFlipAxis

class FontAwesomeIconFlipEffect(FontAwesomeIconBaseEffect):

    def __init__(self, parent_surface: pygame.Surface, icon: FontAwesomeIcons, font_path: Optional[str] = None, size: int = 16, color: tuple[int, int, int] = (255, 255, 255), speed: FontAwesomeAnimationSpeed = FontAwesomeAnimationSpeed.MEDIUM, axis: FontAwesomeAnimationFlipAxis = FontAwesomeAnimationFlipAxis.HORIZONTAL) -> None:
        super().__init__(parent_surface = parent_surface, icon = icon, font_path = font_path, size = size, color = color, speed = speed)
        if axis == FontAwesomeAnimationFlipAxis.HORIZONTAL:
            self._animation_type = FontAwesomeAnimationType.HORIZONTAL_FLIP
        else:
            self._animation_type = FontAwesomeAnimationType.VERTICAL_FLIP
        self.__flip = False
        self.__icon_surface = super().render(self._icon, self._color)
        self.__real_surface_size = self.__icon_surface.get_size()
        self.__icon_surface_flipped = pygame.transform.flip(self.__icon_surface, self._animation_type == FontAwesomeAnimationType.HORIZONTAL_FLIP, self._animation_type == FontAwesomeAnimationType.VERTICAL_FLIP)
        self.__width = self.__icon_surface.get_width()
        self.__current_width = self.__width
        self.__last_width = self.__current_width
        self.__height = self.__icon_surface.get_height()
        self.__current_height = self.__height
        self.__last_height = self.__current_height
        self.__shrinking = True
        self._set_total_frames((self.__width if self._animation_type == FontAwesomeAnimationType.HORIZONTAL_FLIP else self.__height) * 4)

    def _animate(self) -> None:
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
                if self.__current_width >= self.__width:
                    self.__current_width = self.__width
                    self.__shrinking = True
            else:
                self.__current_height += self._frame_skip
                if self.__current_height >= self.__height:
                    self.__current_height = self.__height
                    self.__shrinking = True
        return True

    @property
    def _changed(self) -> bool:
        if self._animation_type == FontAwesomeAnimationType.HORIZONTAL_FLIP:
            return self.__last_width != int(self.__current_width)
        else:
            return self.__last_height != int(self.__current_height)

    def _update_changed_values(self) -> None:
        if self._animation_type == FontAwesomeAnimationType.HORIZONTAL_FLIP:
            self.__last_width = int(self.__current_width)
        else:
            self.__last_height = int(self.__current_height)

    def _render_animation(self) -> pygame.Surface:
        tmp_surface = pygame.Surface(self.__real_surface_size, pygame.SRCALPHA)
        streched_icon = pygame.transform.scale(self.__icon_surface if self.__flip else self.__icon_surface_flipped, (self.__current_width, self.__current_height))
        if self._animation_type == FontAwesomeAnimationType.HORIZONTAL_FLIP:
            dest = ((self.__width - self.__current_width) // 2, 0)
        else:
            dest = (0, (self.__height - self.__current_height) // 2)
        tmp_surface.blit(streched_icon, dest)
        return tmp_surface
