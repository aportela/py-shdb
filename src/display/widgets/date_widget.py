import pygame

from .Widget import Widget
import datetime

class DateWidget(Widget):

    def __init__(self, name: str, x: int , y: int, width: int, height: int, padding: int, surface: pygame.Surface, debug: bool, font_family: str, font_size: int, font_color: tuple, format_mask: str = "%A, %B %d"):
        super().__init__(name=name, surface=surface, debug=debug, x=x, y=y, width=width, height=height, padding=padding)
        self._font = pygame.font.SysFont(font_family, font_size, bold = True) # TODO: font bold style (or italic) on params
        self._font_color = font_color
        self._format_mask = format_mask
        self._str = None

    def refresh(self, force: bool = False) -> bool:
        now = datetime.datetime.now()
        new_str = now.strftime(self._format_mask)
        if (force or self._str != new_str):
            self._str == new_str
            self.clear()
            self._tmp_surface.blit(
                self._font.render(new_str.title(), True, self._font_color),
                (self._padding, self._padding)
            )
            super().render()
            return True
        else:
            return False
