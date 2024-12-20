import os
import pygame
from .font_awesome_unicode_icons import FontAwesomeUnicodeIcons

class FontAwesomeIcon():
    def __init__(self, file: str, size: int, color: tuple = (255, 255, 255)) -> None:
        if not os.path.exists(file):
            raise ValueError(f"font awesome external file {file} not found.")
        self._font = pygame.font.Font(file, size)
        self.__file = file
        self.__size = size
        self.__color = color

    def set_size(self, size: int):
        self.__size = size
        self._font = pygame.font.Font(self.__file, self.__size)

    def set_color(self, color: tuple):
        self.__color = color

    def render(self, icon: FontAwesomeUnicodeIcons, custom_color: tuple = None) -> pygame.Surface:
        return self._font.render(icon, True, (custom_color if custom_color else self.__color))
