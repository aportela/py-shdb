import pygame
from .widget import Widget
from .widget_font import WidgetFont

SEPARATOR = "#"

class HorizontalTickerWidget(Widget):

    def __init__(self, name: str, x: int , y: int, width: int, height: int, padding: int, border: bool = False, surface: pygame.Surface = None, font: WidgetFont = None, text: str = None, speed: int = 1):
        # Initialize the parent class (Widget) with the provided parameters.
        super().__init__(name = name, x = x, y = y, width = width, height = height, padding = padding, border = border, surface = surface)

        # Check if the font is provided, otherwise raise an error
        if font == None:
            raise RuntimeError("Font not set")  # Font must be provided
        else:
            self.__font = font  # Set the font

        if (text == None):
            raise RuntimeError("Text not set")
        self.__text_surface = self.__font.render(f"{text} {SEPARATOR} ")
        self.__speed = speed
        self.__x_offset = 0
        self.__y_offset = (self._height - self.__text_surface.get_height()) // 2
        self.__render_required = True # TODO: control changes with frames/ticks

    def refresh(self, force: bool = False) -> bool:
        if force or self.__render_required:
            self._clear()
            text_width = self.__text_surface.get_width()
            num_repeats = (self._width // text_width) + 2
            for i in range(num_repeats):
                x_position = self.__x_offset + i * text_width
                self._blit(self.__text_surface, (x_position, self.__y_offset - self._padding))
            self.__x_offset -= self.__speed
            if self.__x_offset < -text_width:
                self.__x_offset += text_width
            super()._render()
        return True
