import pygame

from .Widget import Widget
from ...modules.rss.rss_feed import RSSFeed

class RSSWidget(Widget):

    def __init__(self, surface: pygame.Surface, debug: bool = False, x: int = 0, y: int = 0, width: int = 0, height: int = 0, padding: int = 0, font_family: str = "monospace", font_size: int = 12, url: str = "", default_seconds_refresh_time: int = 600, max_items: int = 16):
        # Llamada al constructor de la clase base
        super().__init__(surface=surface, debug=debug, x=x, y=y, width=width, height=height, padding=padding)
        self._font = pygame.font.SysFont(font_family, font_size, bold = True)
        self._module = RSSFeed(url, default_seconds_refresh_time, max_items)
        # TODO: try / except
        self._module.get(True)

    def refresh(self, force: bool = False) -> bool:

        # TODO: try / except
        data = self._module.get(False)

        if (force or data["changed"]):
            self.clear()
            title_text = self._font.render(data["title"], True, (255, 255, 255))
            y = self._padding
            self._tmp_surface.blit(title_text, (self._padding, y))
            y += title_text.get_height() + 4
            for item in data["items"]:
                item_text = self._font.render(item["title"], True, (255, 255, 255))
                self._tmp_surface.blit(item_text, (self._padding, y))
                y += title_text.get_height() + 4
            super().blit()
            return True
        else:
            return False
