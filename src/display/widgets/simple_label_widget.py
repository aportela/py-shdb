import pygame

from .widget import Widget
from .widget_font import WidgetFont

class SimpleLabelWidget(Widget):

    def __init__(self, name: str, x: int, y: int, width: int, height: int, padding: int, border: bool = False, surface: pygame.Surface = None, font: WidgetFont = None, text: str = None):
        # Initialize the parent class (Widget) with the provided parameters
        super().__init__(name=name, x=x, y=y, width=width, height=height, padding=padding, border=border, surface=surface)

        # Ensure that the font is provided, otherwise raise an error
        if font is None:
            raise RuntimeError("Font not set")  # Font must be provided
        else:
            self.__font = font  # Set the font for rendering text

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
            self._clear()  # Clear the previous content

            # Render the text using the specified font and blit it to the surface
            self._blit(self.__font.render(self._text))

            # Call the parent class to handle additional rendering logic
            super()._render()
            return True  # Indicate that the widget was rendered successfully
        else:
            return False  # Return False if the widget doesn't need a refresh
