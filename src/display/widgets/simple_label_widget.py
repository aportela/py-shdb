import pygame

from .widget import Widget
from .widget_font import WidgetFont

class SimpleLabelWidget(Widget):

    def __init__(self, name: str, x: int , y: int, width: int, height: int, padding: int, border: bool = False, surface: pygame.Surface = None, font: WidgetFont = None, text: str = None):
        # Initialize the parent class (Widget) with the provided parameters
        super().__init__(name = name, x = x, y = y, width = width, height = height, padding = padding, border = border, surface = surface)
                # Ensure that the font is provided, otherwise raise an error
        if font is None:
            raise RuntimeError("Font not set")  # Font must be provided
        else:
            self.__font = font  # Set the font for rendering text

        # Ensure that the text is provided, otherwise raise an error
        if text is None:
            raise RuntimeError("Text not set")  # Text must be provided
        self._text = text
        self._render_required = True # this widget has static text (no changes) so only render on first refresh iteration

    def refresh(self, force: bool = False) -> bool:
        if force or self._render_required:
            self._render_required = False
            self._clear()
            self._blit(self.__font.render(self._text))
            super()._render()
            return True
        else:
            return False
