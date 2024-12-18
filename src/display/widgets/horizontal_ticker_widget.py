import pygame
from .widget import Widget
from .widget_font import WidgetFont

# Separator character used to separate text in the ticker
SEPARATOR = "#"

class HorizontalTickerWidget(Widget):

    def __init__(self, name: str, x: int , y: int, width: int, height: int, padding: int, background_color: tuple[int, int, int, int] = (0, 0, 0, 0), border: bool = False, surface: pygame.Surface = None, font: WidgetFont = None, text: str = None, speed: int = 1):
        # Initialize the parent class (Widget) with the provided parameters
        super().__init__(name = name, x = x, y = y, width = width, height = height, padding = padding, background_color = background_color, border = border, surface = surface)

        # Ensure that the font is provided, otherwise raise an error
        if font is None:
            raise RuntimeError("Font not set")  # Font must be provided
        else:
            self.__font = font  # Set the font for rendering text

        # Ensure that the text is provided, otherwise raise an error
        if text is None:
            raise RuntimeError("Text not set")  # Text must be provided
        # Render the text with the font and add a separator to the end
        self.__text_surface = self.__font.render(f"{text} {SEPARATOR} ")

        # Set the speed at which the text moves
        self.__speed = speed

        # Initial horizontal offset (starting position of the text)
        self.__x_offset = 0

        # Calculate the vertical offset to vertically center the text in the widget
        self.__y_offset = (self._height - self.__text_surface.get_height()) // 2

        # Flag indicating whether a render is required
        self.__render_required = True  # TODO: Control changes with frames/ticks

    def refresh(self, force: bool = False) -> bool:
        """
        Refreshes the widget by updating the horizontal ticker's position and redrawing the text.

        :param force: If True, forces the widget to refresh even if no changes occurred.
        :return: True if the widget was refreshed successfully, False otherwise.
        """

        # If forced or if render is required (e.g., animation), redraw the ticker
        if force or self.__render_required:
            # Clear the previous content
            self._clear()

            # Get the width of the rendered text
            text_width = self.__text_surface.get_width()

            # Calculate how many times to repeat the text across the width of the widget
            num_repeats = (self._width // text_width) + 2  # Extra repetitions for smooth scrolling

            # Loop through and render the text at the appropriate horizontal position
            for i in range(num_repeats):
                # Calculate the horizontal position of the text based on the offset
                x_position = self.__x_offset + i * text_width

                # Blit (draw) the text surface at the calculated position (with padding applied)
                self._blit(self.__text_surface, (x_position, self.__y_offset - self._padding))

            # Update the horizontal offset to make the text scroll
            self.__x_offset -= self.__speed

            # If the text has completely scrolled off to the left, reset the offset to the right
            if self.__x_offset < -text_width:
                self.__x_offset += text_width

            # Render the widget on the surface
            super()._render()

        return True
