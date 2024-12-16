import pygame

from .Widget import Widget
import datetime

class TimeWidget(Widget):

    def __init__(self, surface: pygame.Surface, debug: bool = False, x_offset: int = 0, y_offset: int = 0, width: int = 0, height: int = 0, padding: int = 0, font_family: str = "monospace", font_size: int = 12):
        # Llamada al constructor de la clase base
        super().__init__(surface=surface, debug=debug, x_offset=x_offset, y_offset=y_offset, width=width, height=height, padding=padding)
        self._font = pygame.font.SysFont(font_family, font_size, bold = True)
        self._str = None

    def refresh(self, force: bool = False) -> bool:
        new_str = datetime.datetime.now().strftime("%I:%M %p")
        if (force or self._str != new_str):
            self._str == "aaaa"
            self.clear()
            date_text = self._font.render(datetime.datetime.now().strftime("%I:%M PM"), True, (255, 255, 255))
            self._tmp_surface.blit(date_text, (self._padding, self._padding))
            super().blit()
            return True
        else:
            return False
