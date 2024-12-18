import pygame
import datetime

from .widget import Widget
from .widget_font import WidgetFont

class DateWidget(Widget):

    def __init__(self, name: str, x: int , y: int, width: int, height: int, padding: int, background_color: tuple[int, int, int, int] = (0, 0, 0, 0), border: bool = False, surface: pygame.Surface = None, font: WidgetFont = None, format_mask: str = "%A, %B %d"):
        # Initialize the parent class (Widget) with the provided parameters.
        super().__init__(name = name, x = x, y = y, width = width, height = height, padding = padding, background_color = background_color, border = border, surface = surface)

        # Check if the font is provided, otherwise raise an error
        if font == None:
            raise RuntimeError("Font not set")  # Font must be provided
        else:
            self.__font = font  # Set the font

        # Set the date format mask (the format in which the date will be displayed)
        self.__format_mask = format_mask

        # Initialize the string that will hold the formatted date
        self.__str = None

    def refresh(self, force: bool = False) -> bool:
        """
        Refreshes the widget with the current date. If the date has changed or if forced,
        the widget is redrawn with the new date string.

        :param force: If True, forces the widget to refresh even if the date hasn't changed.
        :return: Returns True if the widget was successfully refreshed, False otherwise.
        """

        # Get the current date and format it according to the specified format mask
        new_str = datetime.datetime.now().strftime(self.__format_mask).title()

        # If forced or if the date has changed, update the widget
        if force or self.__str != new_str:
            self.__str = new_str  # Update the stored date string

            # Clear the previous content
            self._clear()

            # Render the new date string and place it in the widget
            super()._blit(self.__font.render(new_str))

            # Render the widget on the surface
            super()._render()

            return True  # Indicate that the widget was refreshed
        else:
            return False  # No change in the date, so no refresh needed

    def on_click(self):
        self._log.debug("detected widget click event, forcing refresh")
        self.refresh(True)
