import pygame

from .Widget import Widget

class Example(Widget):
    def __init__(self, surface: pygame.Surface, debug: bool = False, x_offset: int = 0, y_offset: int = 0, width: int = 0, height: int = 0, padding: int = 0):
        # Llamada al constructor de la clase base
        super().__init__(surface=surface, debug=debug, x_offset=x_offset, y_offset=y_offset, width=width, height=height, padding=padding)
        self.refresh(True)

    def refresh(self, force: bool = False) -> bool:
        if (force):
            self.clear()
            pygame.draw.rect(self._tmp_surface, (255, 100, 255), (self._padding, self._padding, self._width / 2, self._height / 2))
            # print(f"Refreshed")
            super().blit()
            return True
        else:
            return False
