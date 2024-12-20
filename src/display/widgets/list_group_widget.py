import pygame
from typing import List, Optional

from .widget import Widget, DEFAULT_WIDGET_BORDER_COLOR
from .widget_font import WidgetFont

class ListGroupWidget(Widget):

    def __init__(self, name: str, x: int, y: int, width: int, height: int, padding: int, background_color: tuple[int, int, int, int] = (0, 0, 0, 0), border: bool = False, surface: pygame.Surface = None, title_font: WidgetFont = None, title_text: str = None, items_font: WidgetFont = None, items_text: Optional[List[str]] = None) -> None:
        super().__init__(surface = surface, name = name, x = x, y = y, width = width, height = height, padding = padding, background_color = background_color, border = border, border_color = border_color)
        if not font:
            raise RuntimeError("Font not set")
        self.__font = font

        # Ensure that the text is provided, otherwise raise an error
        if text is None:
            raise RuntimeError("Text not set")  # Text must be provided
        self._text = text

        # Initialize the render flag. This widget has static text (no changes) so only render on the first refresh iteration
        self._render_required = True

    def refresh(self, force: bool = False) -> bool:
        """
        Refreshes the widget by rendering the text if necessary.
        If the 'force' argument is True or if a render is required,
        the widget will be rendered.
        Otherwise, it won't refresh.
        """
        if force or self._render_required:
            self._render_required = False  # Set the render flag to False since we are rendering the widget
            super()._clear()  # Clear the previous content

            # Render the text using the specified font and blit it to the surface
            self._blit(self.__font.render(self._text))

            # Call the parent class to handle additional rendering logic
            super()._render()
            return True  # Indicate that the widget was rendered successfully
        else:
            return False  # Return False if the widget doesn't need a refresh

    def on_click(self):
        self._log.debug("detected widget click event, forcing refresh")
        self.refresh(True)
