from typing import Optional
import pygame

from .widget import Widget, DEFAULT_WIDGET_BORDER_COLOR
from .widget_font import WidgetFont

class SimpleLabelWidget(Widget):

    def __init__(self, parent_surface: pygame.Surface, name: str, rect: pygame.Rect, background_color: tuple[int, int, int] = None, border: bool = False, border_color: tuple[int, int, int] = DEFAULT_WIDGET_BORDER_COLOR, font: WidgetFont = None, text: Optional[str] = None) -> None:
        super().__init__(parent_surface = parent_surface, name = name, rect = rect, background_color = background_color, border = border, border_color = border_color)
        if not font:
            raise RuntimeError("Font not set")
        self.__font = font
        if not text:
            raise RuntimeError("Text not set")
        self.__text = text
        self.__render_required = True

    def refresh(self, force: bool = False) -> bool:
        if force or self.__render_required:
            self.__render_required = False
            super()._clear()
            super()._blit(self.__font.render(self.__text))
            super()._render()
            return True
        else:
            return False

    def on_click(self):
        self._log.debug("detected widget click event, forcing refresh")
        self.refresh(True)
