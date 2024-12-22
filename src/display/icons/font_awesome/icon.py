from typing import Optional
import os
import pygame
from .icon_list import IconList as FontAwesomeIcons

from ....utils.logger import Logger

class Icon():

    __default_font_file_path = None

    def __init__(self, font_file_path: Optional[str] = None, size: int = 16, color: tuple = (255, 255, 255)) -> None:
        if font_file_path is not None:
            if not os.path.exists(font_file_path):
                raise ValueError(f"Font awesome external file path {font_file_path} not found.")
            else:
                Icon.__default_font_file_path = font_file_path
        elif Icon.__default_font_file_path is None:
            raise ValueError(f"Font awesome external file path not set.")
        self.__font_file_path = font_file_path
        self.__size = size
        self.__color = color
        self._font = pygame.font.Font(font_file_path, size)

    @staticmethod
    def set_default_font_filepath(font_file_path) -> None:
        if os.path.exists(font_file_path):
            Icon.__default_font_file_path = font_file_path
            Logger().debug(f"Setting default FontAwesome path: {font_file_path}")

        else:
            raise ValueError(f"Font awesome external file {font_file_path} not found.")

    def set_size(self, size: int):
        self.__size = size
        self._font = pygame.font.Font(self.__font_file_path, self.__size)

    def set_color(self, color: tuple):
        self.__color = color

    def render(self, icon: FontAwesomeIcons, custom_color: tuple[int, int, int] = None) -> pygame.Surface:
        return self._font.render(icon, True, (custom_color if custom_color else self.__color))
