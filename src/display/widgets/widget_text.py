from typing import Optional
import pygame
from .widget_font import WidgetFont

class WidgetText:
    def __init__(self, font: WidgetFont = None, text: Optional[str] = None) -> None:
        # Ensure that the font is provided, otherwise raise an error
        if font is None:
            raise RuntimeError("Font not set")  # Font must be provided
        else:
            self.__font = font  # Set the font for rendering text
        self.__text = text

    @property
    def text(self) -> str:
        return self.__str

    def set_text(self, text: Optional[str] = None) -> None:
        self.__text = text

    def render(self) -> pygame.Surface:
        return self.__font.render(self.__text, True, self.__font.color)