import pygame
import calendar
from datetime import datetime
import locale

from .widget import Widget, DEFAULT_WIDGET_BORDER_COLOR
from .widget_font import WidgetFont

class MonthCalendarWidget(Widget):
    def __init__(self, surface: pygame.Surface, name: str, x: int , y: int, width: int, height: int, padding: int, background_color: tuple[int, int, int, int] = (0, 0, 0, 0), border: bool = False, border_color: tuple[int, int, int] = DEFAULT_WIDGET_BORDER_COLOR, font: WidgetFont = None, year: int = None, month: int = None) -> None:
        super().__init__(surface = surface, name = name, x = x, y = y, width = width, height = height, padding = padding, background_color = background_color, border = border, border_color = border_color)
        if not font:
            raise RuntimeError("Font not set")
        self.__font = font
        self.__current_date = datetime.now() if not year or not month else datetime(year, month, 1)

        self.__days_in_month = calendar.monthrange(self.__current_date.year, self.__current_date.month)[1]
        self.__first_day_of_week = calendar.monthrange(self.__current_date.year, self.__current_date.month)[0]

        self._calendar_grid = self._generate_calendar_grid()

        self._set_locale_days()

        self._render_required = True

    def _set_locale_days(self):
        locale.setlocale(locale.LC_TIME, '')
        self._week_days = [calendar.day_name[i][:3] for i in range(7)]

    def _generate_calendar_grid(self):
        grid = [['' for _ in range(7)] for _ in range(6)]
        current_day = 1

        for row in range(6):
            for col in range(7):
                if row == 0 and col < self.__first_day_of_week:
                    continue
                if current_day > self.__days_in_month:
                    break
                grid[row][col] = current_day
                current_day += 1
        return grid

    def refresh(self, force: bool = False) -> bool:
        if force or self._render_required:
            self._render_required = False
            super()._clear()

            x_offset = self.padding
            y_offset = self.padding

            for i, day in enumerate(self._week_days):
                day_surface = self.__font.render(day.title())
                day_width = day_surface.get_width()
                x_position = x_offset + i * (self.width // 7) + (self.width // 7 - day_width)
                self._blit(day_surface, (x_position, y_offset))

            y_offset += 30

            today = self.__current_date.day

            for row in range(6):
                for col in range(7):
                    day = self._calendar_grid[row][col]
                    if day != '':
                        day_surface = self.__font.render(str(day))
                        day_height = day_surface.get_height()
                        y_position = y_offset + row * 30 + (30 - day_height) // 2
                        day_width = day_surface.get_width()
                        x_position = x_offset + col * (self.width // 7) + (self.width // 7 - day_width)
                        if day == today:
                            pygame.draw.rect(self._tmp_surface, (255, 255, 255), (x_offset + col * (self.width // 7), y_offset + row * 30, self.width // 7, 30), 1)
                        self._blit(day_surface, (x_position, y_position))
            super()._render()
            return True
        else:
            return False

    def on_click(self):
        self._log.debug("detected widget click event, forcing refresh")
        self.refresh(True)
