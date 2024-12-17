import pygame
import calendar
from datetime import datetime
import locale

from .widget import Widget
from .widget_font import WidgetFont

class MonthCalendarWidget(Widget):
    def __init__(self, name: str, x: int , y: int, width: int, height: int, padding: int, border: bool = False, surface: pygame.Surface = None, font: WidgetFont = None, year: int = None, month: int = None):
        # Initialize the parent class (Widget) with the provided parameters
        super().__init__(name = name, x = x, y = y, width = width, height = height, padding = padding, border = border, surface = surface)

        # Ensure that the font is provided, otherwise raise an error
        if font is None:
            raise RuntimeError("Font not set")  # Font must be provided
        else:
            self.__font = font  # Set the font for rendering text

        # Set the current date if year and month are not provided, otherwise use the provided values
        self._current_date = datetime.now() if not year or not month else datetime(year, month, 1)

        # Get the number of days in the month and the first day of the week
        self._days_in_month = calendar.monthrange(self._current_date.year, self._current_date.month)[1]
        self._first_day_of_week = calendar.monthrange(self._current_date.year, self._current_date.month)[0]

        # Generate the grid to represent the calendar (6 rows, 7 columns)
        self._calendar_grid = self._generate_calendar_grid()

        # Set the current locale and get the localized week days
        self._set_locale_days()

        # Flag to indicate if rendering is required
        self._render_required = True

    def _set_locale_days(self):
        """Sets the week days based on the current locale"""
        locale.setlocale(locale.LC_TIME, '')  # Set the system's default locale
        # Get the first three letters of each weekday name (localized)
        self._week_days = [calendar.day_name[i][:3] for i in range(7)]  # Get abbreviated day names

    def _generate_calendar_grid(self):
        """Generates a grid with the dates of the month"""
        # Create a 6x7 grid for the calendar (6 rows, 7 columns)
        grid = [['' for _ in range(7)] for _ in range(6)]
        current_day = 1

        # Fill the grid with the days of the month
        for row in range(6):
            for col in range(7):
                if row == 0 and col < self._first_day_of_week:  # Skip days before the first day of the month
                    continue
                if current_day > self._days_in_month:  # Stop if we exceed the number of days in the month
                    break
                grid[row][col] = current_day  # Assign the day number to the grid
                current_day += 1
        return grid

    def refresh(self, force: bool = False) -> bool:
        # Render the calendar only if rendering is required or forced
        if force or self._render_required:
            self._render_required = False
            self._clear()

            x_offset = self._padding  # Add horizontal padding offset
            y_offset = self._padding  # Add vertical padding offset

            # Draw the week days using the current locale settings
            for i, day in enumerate(self._week_days):
                day_surface = self.__font.render(day.title())  # Capitalize the first letter of each day name
                # Calculate the horizontal position to align the day name to the right
                day_width = day_surface.get_width()
                x_position = x_offset + i * (self._width // 7) + (self._width // 7 - day_width)  # Align text to the right
                self._blit(day_surface, (x_position, y_offset))

            y_offset += 30  # Move the Y offset down after drawing the week days

            # Get the current day of the month
            today = self._current_date.day

            # Draw the days of the month
            for row in range(6):
                for col in range(7):
                    day = self._calendar_grid[row][col]
                    if day != '':  # Skip empty cells
                        day_surface = self.__font.render(str(day))  # Render the day number
                        # Calculate the vertical position to center the number in the cell
                        day_height = day_surface.get_height()
                        y_position = y_offset + row * 30 + (30 - day_height) // 2  # Center the text vertically

                        # Calculate the horizontal position to align the text to the right
                        day_width = day_surface.get_width()
                        x_position = x_offset + col * (self._width // 7) + (self._width // 7 - day_width)  # Align text to the right

                        # Highlight the current day with a white border of 1px
                        if day == today:
                            # Draw a rectangle around the current day (white border)
                            pygame.draw.rect(self._tmp_surface, (255, 255, 255),
                                             (x_offset + col * (self._width // 7), y_offset + row * 30, self._width // 7, 30), 1)  # White border with 1px width

                        # Draw the day number at the calculated position
                        self._blit(day_surface, (x_position, y_position))

            # Call the parent render method
            super()._render()
            return True
        else:
            return False
