import pygame
import datetime

from .widget import Widget, DEFAULT_WIDGET_BORDER_COLOR
from .widget_font import WidgetFont

class DateWidget(Widget):

    def __init__(self, parent_surface: pygame.Surface, name: str, x: int, y: int, width: int, height: int, padding: int, background_color: tuple[int, int, int] = None, border: bool = False, border_color: tuple[int, int, int] = DEFAULT_WIDGET_BORDER_COLOR, font: WidgetFont = None, format_mask: str = "%A, %B %d") -> None:
        super().__init__(parent_surface = parent_surface, name = name, x = x, y = y, width = width, height = height, padding = padding, background_color = background_color, border = border, border_color = border_color)
        if not font:
            raise RuntimeError("Font not set")
        self.__font = font
        self.__format_mask = format_mask
        self.__text = None

    def refresh(self, force: bool = False) -> bool:
        new_text = datetime.datetime.now().strftime(self.__format_mask).title()
        if force or self.__text != new_text:
            self.__text = new_text
            super()._clear()
            super()._blit(self.__font.render(self.__text))
            super()._render()
            return True
        else:
            return False

    def on_click(self):
        self._log.debug("Detected widget click event, forcing refresh")
        self.refresh(True)
