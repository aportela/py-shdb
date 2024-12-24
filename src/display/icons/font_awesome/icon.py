from typing import Optional
import os
import pygame
from .icon_list import IconList as FontAwesomeIcon

from ....utils.logger import Logger

class Icon():

    __default_font_path = None

    def __init__(self, font_path: Optional[str] = None, size: int = 16, color: tuple[int, int, int] = (255, 255, 255)) -> None:
        if font_path is not None:
            if not os.path.exists(font_path):
                raise ValueError(f"Font awesome external file path {font_path} not found.")
            else:
                Icon.__default_font_path = font_path
        elif Icon.__default_font_path is None:
            raise ValueError(f"Font awesome external file path not set.")
        self.__font_path = font_path
        self.__size = size
        self.__color = color
        self._font = pygame.font.Font(font_path, size)

    @staticmethod
    def set_default_font_path(font_path) -> None:
        if os.path.exists(font_path):
            Icon.__default_font_path = font_path
            Logger().debug(f"Setting default FontAwesome path: {font_path}")
        else:
            raise ValueError(f"Font awesome external file {font_path} not found.")

    def set_size(self, size: int) -> None:
        self.__size = size
        self._font = pygame.font.Font(self.__font_path, self.__size)

    def set_color(self, color: tuple[int, int, int]) -> None:
        self.__color = color

    def render(self, icon: FontAwesomeIcon, custom_color: tuple[int, int, int] = None) -> pygame.Surface:
        return self._font.render(icon, True, (custom_color if custom_color else self.__color))
