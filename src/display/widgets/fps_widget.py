import pygame

from .widget import Widget, DEFAULT_WIDGET_BORDER_COLOR
from .widget_font import WidgetFont
from ..fps import FPS

class FPSWidget(Widget):

    def __init__(self, parent_surface: pygame.Surface, name: str, x: int , y: int, width: int, height: int, background_color: tuple[int, int, int] = None, border: bool = False, border_color: tuple[int, int, int] = DEFAULT_WIDGET_BORDER_COLOR, font: WidgetFont = None) -> None:
        super().__init__(parent_surface = parent_surface, name = name, x = x, y = y, width = width, height = height, background_color = background_color, border = border, border_color = border_color)
        if not font:
            raise RuntimeError("Font not set")
        self.__font = font
        self.__previousFPS = None

    def refresh(self, force: bool = False) -> bool:
        current_fps = FPS.get_current_fps()
        if force or self.__previousFPS != current_fps:
            self.__previousFPS = current_fps
            super()._clear()
            super()._blit(self.__font.render(f"FPS: {current_fps:03d}"))
            super()._render()
            return True
        else:
            return False

    def on_click(self):
        self._log.debug("Detected widget click event, forcing refresh")
        self.refresh(True)
