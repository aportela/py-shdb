from enum import Enum
import pygame

from .widget import Widget, DEFAULT_WIDGET_BORDER_COLOR
from .widget_font import WidgetFont

# Separator character used to separate text in the ticker
SEPARATOR = "#"

class HorizontalTickerSpeed(Enum):
    NORMAL: 1
    MEDIUM: 2
    FAST  : 4

class HorizontalTickerWidget(Widget):

    def __init__(self, surface: pygame.Surface, name: str, x: int, y: int, width: int, height: int, padding: int, background_color: tuple[int, int, int] = None, border: bool = False, border_color: tuple[int, int, int] = DEFAULT_WIDGET_BORDER_COLOR, font: WidgetFont = None, text: str = None, speed: int = 1) -> None:
        super().__init__(surface = surface, name = name, x = x, y = y, width = width, height = height, padding = padding, background_color = background_color, border = border, border_color = border_color)
        if not font:
            raise RuntimeError("Font not set")
        self.__font = font
        if not text:
            raise RuntimeError("Text not set")
        self.__text_surface = self.__font.render(f"{text} {SEPARATOR} ")
        self.__speed = speed
        self.__x_offset = 0
        self.__y_offset = (self.height - self.__text_surface.get_height()) // 2
        self.__render_required = True

    def refresh(self, force: bool = False) -> bool:
        if force or self.__render_required:
            super()._clear()
            text_width = self.__text_surface.get_width()
            num_repeats = (self.width // text_width) + 2
            for i in range(num_repeats):
                x_position = self.__x_offset + i * text_width
                self._blit(self.__text_surface, (x_position, self.__y_offset - self.padding))
            self.__x_offset -= self.__speed
            if self.__x_offset < -text_width:
                self.__x_offset += text_width
            super()._render()
        return True

    def on_click(self):
        self._log.debug("detected widget click event, forcing refresh")
        self.__x_offset = 0
        self.refresh(True)
