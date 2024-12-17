import pygame
import datetime

from .widget import Widget
from .widget_font import WidgetFont

class TimeWidget(Widget):

    def __init__(self, name: str, x: int , y: int, width: int, height: int, padding: int, surface: pygame.Surface, debug: bool, font: WidgetFont, format_mask: str = "%I:%M %p"):
        super().__init__(name=name, surface=surface, debug=debug, x=x, y=y, width=width, height=height, padding=padding)
        self._font = font
        self._format_mask = format_mask
        self._str = None

    def refresh(self, force: bool = False) -> bool:
        now = datetime.datetime.now()
        # ugly hack because depending your system locale %p (AM/FM) will not work
        new_str = now.strftime( self._format_mask.replace("%p", "AM" if now.hour < 12 else "PM")).upper()
        if (force or self._str != new_str):
            self._str == new_str
            self.clear()
            self._tmp_surface.blit(
                self._font.render(new_str),
                (self._padding, self._padding)
            )
            super().render()
            return True
        else:
            return False
