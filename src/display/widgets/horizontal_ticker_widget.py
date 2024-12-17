import pygame
from .widget import Widget
from .widget_font import WidgetFont

SEPARATOR = "#"

class HorizontalTickerWidget(Widget):

    def __init__(self, name: str, x: int , y: int, width: int, height: int, padding: int, surface: pygame.Surface, debug: bool, font: WidgetFont, text: str, speed: int):
        super().__init__(name=name, surface=surface, debug=debug, x=x, y=y, width=width, height=height, padding=padding)
        self._font = font
        self._text = text
        self._text_surface = self._font.render(f"{self._text} {SEPARATOR} ")
        self._speed = speed
        self._x_offset = 0
        self._y_offset = (self._height - self._text_surface.get_height()) // 2
        self._render_required = True

    def refresh(self, force: bool = False) -> bool:
        if force or self._render_required:
            self._clear()

            # Ancho total del texto
            text_width = self._text_surface.get_width()
            num_repeats = (self._width // text_width) + 2  # Aseguramos suficientes repeticiones

            # Dibujar todas las copias necesarias
            for i in range(num_repeats):
                x_position = self._x_offset + i * text_width
                self._tmp_surface.blit(self._text_surface, (x_position, self._y_offset - self._padding))

            # Actualizar posición
            self._x_offset -= self._speed

            # Reiniciar si el texto completo ha salido de la pantalla
            if self._x_offset < -text_width:
                self._x_offset += text_width

            super()._render()
        return True
