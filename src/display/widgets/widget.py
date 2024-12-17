import pygame
from abc import ABC, abstractmethod

WIDGET_BORDER_COLOR=(255, 105, 180)

class Widget(ABC):
    def __init__(self, name: str, x: int , y: int, width: int, height: int, padding: int, surface: pygame.Surface, debug: bool):
        if width < 0 or height < 0 or padding < 0:
            raise ValueError("Invalid width/height/padding")
        self._name = name
        self._debug = debug
        self._surface = surface
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._padding = padding

        # temporal surface for this widget
        self._tmp_surface = pygame.Surface((self._width, self._height))
        self._tmp_surface.fill((0, 0, 0))

    @property
    def name(self) -> str:
        return self._name

    # clear temporal widget surface
    def clear(self):
        self._tmp_surface.fill((0, 0, 0))

    # dump temporal widget surface on main surface
    def render(self):
        if self._debug:
            # add border (for debug sizes/offsets)
            pygame.draw.rect(self._tmp_surface, WIDGET_BORDER_COLOR, (0, 0, self._width , self._height), 1)
        # dump surface
        self._surface.blit(self._tmp_surface, (self._x, self._y))

    @abstractmethod
    def refresh(self, force: bool = False) -> bool:
        """
        abstract method for refreshing widget

        :param force: if true, always refresh (warning, high cpu cost)
        :return: returns true if widget detect changes
        """
        pass
