import pygame
import datetime

from .widget import Widget
from .widget_font import WidgetFont

class DateWidget(Widget):

    def __init__(self, name: str, x: int , y: int, width: int, height: int, padding: int, surface: pygame.Surface, debug: bool, font: WidgetFont, format_mask: str = "%A, %B %d"):
        super().__init__(name=name, surface=surface, debug=debug, x=x, y=y, width=width, height=height, padding=padding)
        self._font = font
        self._format_mask = format_mask
        self._str = None

    def refresh(self, force: bool = False) -> bool:
        now = datetime.datetime.now()
        new_str = now.strftime(self._format_mask).title()
        if (force or self._str != new_str):
            self._str == new_str
            self._clear()
            self._tmp_surface.blit(
                self._font.render(new_str),
                (self._padding, self._padding)
            )
            super()._render()
            return True
        else:
            return False
