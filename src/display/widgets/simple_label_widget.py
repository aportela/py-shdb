import pygame

from .Widget import Widget

class SimpleLabelWidget(Widget):

    def __init__(self, name: str, x: int , y: int, width: int, height: int, padding: int, surface: pygame.Surface, debug: bool, font_family: str, font_size: int, font_color: tuple, text: str):
        super().__init__(name=name, surface=surface, debug=debug, x=x, y=y, width=width, height=height, padding=padding)
        self._font = pygame.font.SysFont(font_family, font_size, bold = True) # TODO: font bold style (or italic) on params
        self._font_color = font_color
        self._text = text
        self._render_required = True # this widget has static text (no changes) so only render on first refresh iteration


    def refresh(self, force: bool = False) -> bool:
        if force or self._render_required:
            self._render_required = False
            self.clear()
            text = self._font.render(self._text, True, self._font_color)
            self._tmp_surface.blit(text, (self._padding, self._padding))
            super().render()
        return False
