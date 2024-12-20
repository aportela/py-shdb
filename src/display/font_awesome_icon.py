from abc import abstractmethod
import os
import pygame
from .font_awesome_unicode_icons import FontAwesomeUnicodeIcons

class FontAwesomeIcon():
    def __init__(self, file: str, size: int, color: tuple = (255, 255, 255)) -> None:
        if not os.path.exists(file):
            raise ValueError(f"font awesome external file {file} not found.")
        self.__font = pygame.font.Font(file, size)
        self.__color = color

    def render(self, icon: FontAwesomeUnicodeIcons, custom_color: tuple = None) -> pygame.Surface:
        return self.__font.render(icon, True, (custom_color if custom_color else self.__color))

    @abstractmethod
    def animate(self) -> pygame.Surface:
        pass
