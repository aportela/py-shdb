import pygame
import datetime

from .widget import Widget
from .widget_font import WidgetFont

class TimeWidget(Widget):

    def __init__(self, name: str, x: int , y: int, width: int, height: int, padding: int, border: bool = False, surface: pygame.Surface = None, font: WidgetFont = None, format_mask: str = "%I:%M %p"):
        # Initialize the parent class (Widget) with the provided parameters
        super().__init__(name = name, x = x, y = y, width = width, height = height, padding = padding, border = border, surface = surface)
        # Ensure that the font is provided, otherwise raise an error
        if font is None:
            raise RuntimeError("Font not set")  # Font must be provided
        else:
            self.__font = font  # Set the font for rendering text
        self._format_mask = format_mask
        self._str = None

    def refresh(self, force: bool = False) -> bool:
        now = datetime.datetime.now()
        # ugly hack because depending your system locale %p (AM/FM) will not work
        new_str = now.strftime( self._format_mask.replace("%p", "AM" if now.hour < 12 else "PM")).upper()
        if (force or self._str != new_str):
            self._str == new_str
            self._clear()
            self._blit(self.__font.render(new_str))
            super()._render()
            return True
        else:
            return False
