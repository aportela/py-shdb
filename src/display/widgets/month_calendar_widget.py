import pygame
import calendar
from datetime import datetime
import locale

from .widget import Widget
from .widget_font import WidgetFont

class MonthCalendarWidget(Widget):
    def __init__(self, name: str, x: int, y: int, width: int, height: int, padding: int, surface: pygame.Surface, debug: bool, font: WidgetFont, year: int = None, month: int = None):
        super().__init__(name=name, surface=surface, debug=debug, x=x, y=y, width=width, height=height, padding=padding)
        self._font = font
        # Set the current month and year if not passed as parameters
        self._current_date = datetime.now() if not year or not month else datetime(year, month, 1)
        self._days_in_month = calendar.monthrange(self._current_date.year, self._current_date.month)[1]
        self._first_day_of_week = calendar.monthrange(self._current_date.year, self._current_date.month)[0]
        self._render_required = True
        self._calendar_grid = self._generate_calendar_grid()

        # Set the current locale and get the week days in the local language
        self._set_locale_days()

    def _set_locale_days(self):
        """Sets the week days based on the current locale"""
        locale.setlocale(locale.LC_TIME, '')  # Set the system's default locale
        self._week_days = [calendar.day_name[i][:3] for i in range(7)]  # Get the first three letters of the day names

    def _generate_calendar_grid(self):
        """Generates a grid with the dates of the month"""
        grid = [['' for _ in range(7)] for _ in range(6)]  # Create a 6x7 grid for the calendar
        current_day = 1
        for row in range(6):
            for col in range(7):
                if row == 0 and col < self._first_day_of_week:  # Skip days before the first day of the month
                    continue
                if current_day > self._days_in_month:  # Stop if we exceed the number of days in the month
                    break
                grid[row][col] = current_day
                current_day += 1
        return grid

    def refresh(self, force: bool = False) -> bool:
        if force or self._render_required:
            self._render_required = False
            self._clear()

            x_offset = self._padding  # Add horizontal padding offset
            y_offset = self._padding  # Add vertical padding offset

            # Draw the week days using the current locale settings
            for i, day in enumerate(self._week_days):
                day_surface = self._font.render(day.title())  # Capitalize the first letter of each day name
                # Calculate the horizontal position to align the day name to the right
                day_width = day_surface.get_width()
                x_position = x_offset + i * (self._width // 7) + (self._width // 7 - day_width)  # Align text to the right
                self._tmp_surface.blit(day_surface, (x_position, y_offset))

            y_offset += 30  # Move the Y offset down after drawing the week days

            # Get the current day of the month
            today = self._current_date.day

            # Draw the days of the month
            for row in range(6):
                for col in range(7):
                    day = self._calendar_grid[row][col]
                    if day != '':
                        day_surface = self._font.render(str(day))
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
                        self._tmp_surface.blit(day_surface, (x_position, y_position))

            super()._render()
            return True
        else:
            return False
