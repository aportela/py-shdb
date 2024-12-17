import pygame
import datetime

from .widget import Widget
from .widget_font import WidgetFont

class DateWidget(Widget):

    def __init__(self, name: str, x: int , y: int, width: int, height: int, padding: int, border: bool = False, surface: pygame.Surface = None, font: WidgetFont = None, format_mask: str = "%A, %B %d"):
        # Initialize the parent class (Widget)
        super().__init__(name = name, x = x, y = y, width = width, height = height, padding = padding, border = border, surface = surface)
        if font == None:
            raise RuntimeError("font not set")
        else:
            self.__font = font
        self.__format_mask = format_mask
        self.__str = None

    def refresh(self, force: bool = False) -> bool:
        new_str = datetime.datetime.now().strftime(self.__format_mask).title()
        if (force or self.__str != new_str):
            self.__str == new_str
            self._clear()
            super()._blit(self.__font.render(new_str))
            super()._render()
            return True
        else:
            return False
