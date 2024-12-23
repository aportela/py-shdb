import pygame
from abc import ABC, abstractmethod
from ...utils.logger import Logger

DEFAULT_WIDGET_BORDER_COLOR=(255, 105, 180) # PINK

class Widget(ABC):
    def __init__(self, parent_surface: pygame.Surface, name: str, x: int, y: int, width: int, height: int, background_color: tuple[int, int, int] = None, border: bool = False, border_color: tuple[int, int, int] = DEFAULT_WIDGET_BORDER_COLOR) -> None:
        self._log = Logger()
        self.__parent_surface = parent_surface
        if not name:
            raise ValueError("Name cannot be None or empty.")
        self.__name = name
        self.__x = x
        self.__y = y
        if width < 1 or height < 1 :
            raise ValueError("Invalid width/height.")
        self.__width = width
        self.__height = height
        self.__widget_area = pygame.Rect(self.__x, self.__y, self.__width, self.__height)
        self.refresh_sub_surface_from_parent_surface()
        self.__background_color = background_color
        self.__border = border
        self.__border_color = border_color
        self.__rect = pygame.Rect(x, y, width, height)
        self._tmp_surface = pygame.Surface((self.__width, self.__height), pygame.SRCALPHA if background_color is None else 0)

    def refresh_sub_surface_from_parent_surface(self) -> None:
        self.__sub_surface = self.__parent_surface.subsurface(self.__widget_area).copy()

    @property
    def parent_surface(self) -> pygame.Surface:
        return self.__parent_surface

    @property
    def name(self) -> str:
        return self.__name

    @property
    def width(self) -> str:
        return self.__width

    @property
    def height(self) -> str:
        return self.__height

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
        self.__parent_surface.blit(self.__sub_surface, self.__widget_area) # clear previous widget area (restoring with original area)
        if self.__border:
            pygame.draw.rect(self._tmp_surface, self.__border_color, (0, 0, self.__width , self.__height), 1)
        self.__parent_surface.blit(self._tmp_surface, self.__widget_area)
        pygame.display.update(self.__widget_area) # update only the widget area

    @abstractmethod
    def refresh(self, force: bool = False) -> bool:
        pass

    def verify_click(self, event):
        if self.__rect.collidepoint(event.pos):
            self.on_click()

    def on_click(self):
        self._log.debug("detected widget click event, but click event not found")
        self.refresh(True)
