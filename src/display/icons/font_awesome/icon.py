from typing import Optional
import os
import pygame

from .icon_list import IconList as FontAwesomeIcon
from ....utils.logger import Logger

class Icon():

    __default_font_path: Optional[str] = None

    def __init__(self, font_path: Optional[str] = None, size: int = 16, color: tuple[int, int, int] = (255, 255, 255)) -> None:
        if font_path is not None:
            if not os.path.exists(font_path):
                raise ValueError(f"Font awesome external file path {font_path} not found.")
            else:
                self.__font_path = font_path
        elif Icon.__default_font_path is None:
            raise ValueError(f"Font awesome external file path not set.")
        self.__size = size
        self.__color = color
        self.__font = self._load_font()

    @staticmethod
    def set_default_font_path(font_path) -> None:
        if os.path.exists(font_path):
            Icon.__default_font_path = font_path
            Logger().debug(f"Setting default FontAwesome font file path: {font_path}")
        else:
            raise ValueError(f"Font awesome font file {font_path} not found.")

    def _load_font(self) -> pygame.font.Font:
        try:
            return pygame.font.Font(self.__font_path, self.__size)
        except Exception as e:
            raise RuntimeError(f"Failed to load font at {self.__font_path}: {e}")

    def set_size(self, size: int) -> None:
        self.__size = size
        self.__font = self._load_font()

    def set_color(self, color: tuple[int, int, int]) -> None:
        self.__color = color

    def render(self, icon: FontAwesomeIcon, custom_color: tuple[int, int, int] = None) -> pygame.Surface:
        color = custom_color if custom_color else self.__color
        return self.__font.render(icon, True, color)
