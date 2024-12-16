import pygame

from .Widget import Widget

class FPSCounter(Widget):

    def __init__(self, surface: pygame.Surface, debug: bool = False, x: int = 0, y: int = 0, width: int = 0, height: int = 0, padding: int = 0, clock: pygame.time.Clock = pygame.time.Clock(), font_family: str = "monospace", font_size: int = 12, position: str = "none"):
        # Llamada al constructor de la clase base
        super().__init__(surface=surface, debug=debug, x=x, y=y, width=width, height=height, padding=padding)
        self._clock = clock
        self._previousFPS = 0
        self._font = pygame.font.SysFont(font_family, font_size)
        self._position = position

    def refresh(self, force: bool = False) -> bool:
        current_fps = int(self._clock.get_fps())
        if (force or current_fps != self._previousFPS):
            self._previousFPS = current_fps
            # TODO: only refresh counter
            fps_text = self._font.render(f"FPS: {current_fps:03d}", True, (255, 255, 0))
            self.clear()
            match self._position:
                case "top_left":
                    self._tmp_surface.blit(fps_text, (8, 8))
                case "top_right":
                    self._tmp_surface.blit(fps_text, (screen.get_width() - fps_text.get_width() - 8, 8))
                case "bottom_left":
                    self._tmp_surface.blit(fps_text, (8, screen.get_height() - fps_text.get_height() - 8))
                case "bottom_right":
                    self._tmp_surface.blit(fps_text, (screen.get_width() - fps_text.get_width() - 8, 8))
                    self._tmp_surface.blit(fps_text, (screen.get_width() - fps_text.get_width() - 8, screen.get_height() - fps_text.get_height() - 8))
            super().blit()
            return True
        else:
            return False
