import pygame
from abc import ABC, abstractmethod
from typing import Optional
from ...utils.logger import Logger

DEFAULT_WIDGET_BORDER_COLOR=(255, 105, 180) # PINK

class Widget(ABC):
    def __init__(self, parent_surface: pygame.Surface, name: str, rect: pygame.Rect, background_color: tuple[int, int, int] = None, border: bool = False, border_color: tuple[int, int, int] = DEFAULT_WIDGET_BORDER_COLOR) -> None:
        self._log = Logger()
        self.__parent_surface = parent_surface
        if not name:
            raise ValueError("Name cannot be None or empty.")
        self.__name = name
        self.__rect = rect
        self.__sub_surface = self.__parent_surface.subsurface(self.__rect).copy()
        self.__background_color = background_color
        self.__border = border
        self.__border_color = border_color
        self._tmp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA if background_color is None else 0)

    @property
    def parent_surface(self) -> pygame.Surface:
        return self.__parent_surface

    @property
    def name(self) -> str:
        return self.__name

    @property
    def x(self) -> str:
        return self.__rect.x

    @property
    def y(self) -> str:
        return self.__rect.y

    @property
    def width(self) -> int:
        return self.__rect.width

    @property
    def height(self) -> int:
        return self.__rect.height

    def _clear(self):
        if self.__background_color is None:
            self._tmp_surface.fill((0, 0, 0, 0))
        else:
            self._tmp_surface.fill(self.__background_color)

    def _blit(self, surface: pygame.Surface, dest: tuple[int, int] = None):
        if dest is None:
            dest = (0, 0)
        self._tmp_surface.blit(surface, dest)

    def _render(self):
        self.__parent_surface.blit(self.__sub_surface, self.__rect) # clear previous widget area (restoring with original area)
        if self.__border:
            pygame.draw.rect(self._tmp_surface, self.__border_color, (0, 0, self.width , self.height), 1)
        self.__parent_surface.blit(self._tmp_surface, self.__rect)
        pygame.display.update(self.__rect) # update only the widget area

    @abstractmethod
    def refresh(self, force: bool = False) -> bool:
        pass

    def verify_click(self, event):
        if self.__rect.collidepoint(event.pos):
            self.on_click()

    def on_click(self):
        self._log.debug("detected widget click event, but click event not found")
        self.refresh(True)
