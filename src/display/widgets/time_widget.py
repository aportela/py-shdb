import pygame
import datetime

from .widget import Widget, DEFAULT_WIDGET_BORDER_COLOR
from .widget_font import WidgetFont

class TimeWidget(Widget):

    def __init__(self, surface: pygame.Surface, name: str, x: int , y: int, width: int, height: int, padding: int, background_color: tuple[int, int, int, int] = (0, 0, 0, 0), border: bool = False, border_color: tuple[int, int, int] = DEFAULT_WIDGET_BORDER_COLOR, font: WidgetFont = None, format_mask: str = "%I:%M %p") -> None:
        super().__init__(surface = surface, name = name, x = x, y = y, width = width, height = height, padding = padding, background_color = background_color, border = border, border_color = border_color)
        if not font:
            raise RuntimeError("Font not set")
        self.__font = font
        self.__format_mask = format_mask
        self.__text = None

    def refresh(self, force: bool = False) -> bool:
        now = datetime.datetime.now()
        new_text = now.strftime(self.__format_mask.replace("%p", "AM" if now.hour < 12 else "PM")).upper()
        if force or self.__text != new_text:
            self.__text = new_text
            super()._clear()
            super()._blit(self.__font.render(new_text))
            super()._render()
            return True
        else:
            return False

    def on_click(self):
        self._log.debug("Detected widget click event, forcing refresh")
        self.refresh(True)
