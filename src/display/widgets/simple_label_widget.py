import pygame

from .widget import Widget
from .widget_font import WidgetFont

class SimpleLabelWidget(Widget):

    def __init__(self, name: str, x: int , y: int, width: int, height: int, padding: int, surface: pygame.Surface, debug: bool, font: WidgetFont, text: str):
        super().__init__(name=name, surface=surface, debug=debug, x=x, y=y, width=width, height=height, padding=padding)
        self._font = font
        self._text = text
        self._render_required = True # this widget has static text (no changes) so only render on first refresh iteration

    def refresh(self, force: bool = False) -> bool:
        if force or self._render_required:
            self._render_required = False
            self.clear()
            self._tmp_surface.blit(
                self._font.render(self._text),
                (self._padding, self._padding)
            )
            super().render()
            return True
        else:
            return False
