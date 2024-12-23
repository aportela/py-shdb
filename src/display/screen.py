import pygame
from ..utils.config import Configuration

class Screen:

    def __init__(self, configuration: Configuration) -> None:
        self.__screen_info = pygame.display.Info()
        self.__screen_resolution = (self.__screen_info.current_w, self.__screen_info.current_h)
        self.__main_surface = pygame.display.set_mode(size = self.__screen_resolution, flags = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.NOFRAME)
        pygame.display.set_caption(configuration.app_name)

    @property
    def width(self) -> int:
        return self.__screen_info.current_w

    @property
    def height(self) -> int:
        return self.__screen_info.current_h
