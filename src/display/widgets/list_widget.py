import pygame

from .widget import Widget, DEFAULT_WIDGET_BORDER_COLOR
from .widget_font import WidgetFont

class ListWidget(Widget):

    def __init__(self, parent_surface: pygame.Surface, name: str, rect: pygame.Rect, background_color: tuple[int, int, int] = None, border: bool = False, border_color: tuple[int, int, int] = DEFAULT_WIDGET_BORDER_COLOR) -> None:
        super().__init__(parent_surface = parent_surface, name = name, rect = rect, background_color = background_color, border = border, border_color = border_color)
        """
        if not font:
            raise RuntimeError("Font not set")
        self.__font = font
        self.__text = None
        """
        self.__refresh_required = True

    def refresh(self, force: bool = False) -> bool:
        if force or self.__refresh_required:
            super()._clear()
            #super()._blit(self.__font.render(new_text))
            super()._render()
            self.__refresh_required = False
            return True
        else:
            return False

    def on_click(self):
        self._log.debug("Detected widget click event, forcing refresh")
        self.refresh(True)
