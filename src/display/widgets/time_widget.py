import pygame
import datetime

from .widget import Widget
from .widget_font import WidgetFont

class TimeWidget(Widget):

    def __init__(self, name: str, x: int , y: int, width: int, height: int, padding: int, background_color: tuple[int, int, int, int] = (0, 0, 0, 0), border: bool = False, surface: pygame.Surface = None, font: WidgetFont = None, format_mask: str = "%I:%M %p"):
        # Initialize the parent class (Widget) with the provided parameters
        super().__init__(name = name, x = x, y = y, width = width, height = height, padding = padding, background_color = background_color, border = border, surface = surface)

        # Ensure that the font is provided, otherwise raise an error
        if font is None:
            raise RuntimeError("Font not set")  # Font must be provided
        else:
            self.__font = font  # Set the font for rendering text

        # Set the format mask to define how the time will be displayed (default: "%I:%M %p")
        self._format_mask = format_mask

        # Initialize a variable to store the previous time string for comparison
        self._str = None

    def refresh(self, force: bool = False) -> bool:
        # Get the current date and time
        now = datetime.datetime.now()

        # Format the time string according to the provided format mask.
        # Fix the issue with system locale by manually setting AM/PM based on the hour
        new_str = now.strftime(self._format_mask.replace("%p", "AM" if now.hour < 12 else "PM")).upper()

        # If forced or the time string has changed, update the display
        if force or self._str != new_str:
            self._str = new_str  # Update the stored time string

            # Clear the widget before rendering the new time
            self._clear()

            # Render and blit the new time string using the specified font
            self._blit(self.__font.render(new_str))

            # Call the parent class render method to handle the actual rendering
            super()._render()

            return True  # Indicate that the widget was refreshed successfully
        else:
            return False  # No update required, time has not changed
