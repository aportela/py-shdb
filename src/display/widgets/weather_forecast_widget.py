import pygame
import math

from .widget import Widget, DEFAULT_WIDGET_BORDER_COLOR
from .widget_font import WidgetFont

class WeatherForecastWidget(Widget):

    def __init__(self, surface: pygame.Surface, name: str, x: int , y: int, width: int, height: int, padding: int, background_color: tuple[int, int, int, int] = (0, 0, 0, 0), border: bool = False, border_color: tuple[int, int, int] = DEFAULT_WIDGET_BORDER_COLOR, font: WidgetFont = None, text: str = None) -> None:
        super().__init__(surface = surface, name = name, x = x, y = y, width = width, height = height, padding = padding, background_color = background_color, border = border, border_color = border_color)
        if not font:
            raise RuntimeError("Font not set")
        self.__font = font
        if not text:
            raise RuntimeError("Text not set")
        self.__text = text
        self._render_required = True
        self.__angle = 0

    def refresh(self, force: bool = False) -> bool:
        radius = 0
        if force or self._render_required:
            super()._clear()  # Clear the previous content
            center = (self.width / 2, self.height / 2)

            icon_surface = self.__font.render(self.__text)
            x = center[0] + radius * math.cos(math.radians(self.__angle))
            y = center[1] + radius * math.sin(math.radians(self.__angle))

            rotated_icon = pygame.transform.rotate(icon_surface, self.__angle)

            rotated_rect = rotated_icon.get_rect(center=(x, y))

            # Render the text using the specified font and blit it to the surface
            super()._blit(rotated_icon, rotated_rect)
            self.__angle = self.__angle + 4
            if self.__angle > 360:
                self.__angle = 0
            # Call the parent class to handle additional rendering logic
            super()._render()
            return True  # Indicate that the widget was rendered successfully
        else:
            return False  # Return False if the widget doesn't need a refresh

    def on_click(self):
        self._log.debug("detected widget click event, forcing refresh")
        self.refresh(True)
