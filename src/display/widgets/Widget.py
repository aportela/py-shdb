import pygame
from abc import ABC, abstractmethod

class Widget(ABC):
    def __init__(self, surface: pygame.Surface, debug: bool = False, x_offset: int = 0, y_offset: int = 0, width: int = 0, height: int = 0, padding: int = 1):
        if width < 0 or height < 0 or padding < 0:
            raise ValueError("Invalid width/height/padding")

        self._debug = debug
        self._surface = surface
        self._x_offset = x_offset
        self._y_offset = y_offset
        self._width = width
        self._height = height
        self._padding = padding
        self._changed = False

        # temporal surface for this widget
        self._tmp_surface = pygame.Surface((self._width, self._height))
        self._tmp_surface.fill((0, 0, 0))

    # clear temporal widget surface
    def clear(self):
        self._tmp_surface.fill((0, 0, 0))

    # dump temporal widget surface on main surface
    def blit(self):
        if self._debug:
            # add border (for debug sizes/offsets)
            pygame.draw.rect(self._tmp_surface, (255, 100, 50), (0, 0, self._width , self._height), 1)
        # dump surface
        self._surface.blit(self._tmp_surface, (self._x_offset, self._y_offset))

    @abstractmethod
    def refresh(self, force: bool = False) -> bool:
        """
        abstract method for refreshing widget

        :param force: if true, always refresh (warning, high cpu cost)
        :return: returns true if widget detect changes
        """
        pass
