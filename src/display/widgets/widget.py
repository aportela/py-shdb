import pygame
from abc import ABC, abstractmethod
from ...utils.logger import Logger

DEFAULT_WIDGET_BORDER_COLOR=(255, 105, 180) # PINK

class Widget(ABC):
    def __init__(self, surface: pygame.Surface, name: str, x: int, y: int, width: int, height: int, padding: int, background_color: tuple[int, int, int] = None, border: bool = False, border_color: tuple[int, int, int] = DEFAULT_WIDGET_BORDER_COLOR) -> None:
        self._log = Logger()
        self.__surface = surface
        if not name:
            raise ValueError("Name cannot be None or empty.")
        self.__name = name
        self.__x = x
        self.__y = y
        if width < 1 or height < 1 or padding < 0:
            raise ValueError("Invalid width/height/padding.")
        self.__width = width
        self.__height = height
        self.__widget_area = pygame.Rect(self.__x, self.__y, self.__width, self.__height)
        self.__sub_surface = self.__surface.subsurface(self.__widget_area)
        self.__padding = padding
        self.__background_color = background_color
        self.__border = border
        self.__border_color = border_color
        self.__rect = pygame.Rect(x, y, width, height)

        self._tmp_surface = pygame.Surface((self.__width, self.__height), pygame.SRCALPHA if background_color is None else 0)
        print(f"Dimensiones de sub-superficie: {self.__sub_surface.get_rect()}")
        print(f"Tamaño de _tmp_surface: {self._tmp_surface.get_size()}")

    @property
    def name(self) -> str:
        return self.__name

    @property
    def width(self) -> str:
        return self.__width

    @property
    def height(self) -> str:
        return self.__height

    @property
    def padding(self) -> str:
        return self.__padding

    def _clear(self):
        if self.__background_color is None:
            self._tmp_surface.fill((0, 0, 0, 0))
        else:
            self._tmp_surface.fill(self.__background_color)

    def _blit(self, surface: pygame.Surface, dest: tuple[int, int] = None):
        if dest is None:
            dest = (self.__padding, self.__padding)
        self._tmp_surface.blit(surface, dest)

    def _render(self):
        if self.__border:
            pygame.draw.rect(self._tmp_surface, self.__border_color, (0, 0, self.__width , self.__height), 1)
        self.__surface.blit(self._tmp_surface, (self.__x, self.__y))

    @abstractmethod
    def refresh(self, force: bool = False) -> bool:
        pass

    def verify_click(self, event):
        if self.__rect.collidepoint(event.pos):
            self.on_click()

    def on_click(self):
        self._log.debug("detected widget click event, but click event not found")
        self.refresh(True)
