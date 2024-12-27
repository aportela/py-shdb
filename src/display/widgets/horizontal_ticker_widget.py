from abc import ABC, abstractmethod
from typing import Optional
from enum import Enum
import pygame

from .widget import Widget, DEFAULT_WIDGET_BORDER_COLOR
from .widget_font import WidgetFont
from ...modules.rss_cache import RSSCache

# Separator character used to separate text in the ticker
SEPARATOR = "#"

class HorizontalTickerSpeed(Enum):
    NORMAL: 1
    MEDIUM: 2
    FAST  : 4

class HorizontalTickerWidgetSource(ABC):
    def __init__(self):
        self._text = None

    @abstractmethod
    def changed(self) -> bool:
        pass

    @abstractmethod
    def reload(self) -> None:
        pass

    @property
    def text(self) -> Optional[str]:
        return self._text

class HorizontalTickerWidgetStringSource(HorizontalTickerWidgetSource):
    def __init__(self, text: Optional[str] = None):
        super().__init__()
        if not text:
            raise RuntimeError("Text not set")
        self._text = text

    def changed(self) -> bool:
        return False

    def reload(self) -> None:
        pass

class HorizontalTickerWidgetRSSSource(HorizontalTickerWidgetSource):
    def __init__(self, cache: RSSCache, item_count: Optional[int] = 16):
        super().__init__()
        self.__cache = cache
        self.__item_count = item_count
        self.__last_change = None
        self.reload()

    def changed(self) -> bool:
        return self.__last_change != self.__cache.last_change

    def reload(self) -> None:
        rss_data = self.__cache.load()
        self.__last_change = self.__cache.last_change
        self._text = " # ".join(f"[{item['published']}] - {item['title']}" for item in rss_data['items'][:self.__item_count])

class HorizontalTickerWidget(Widget):

    def __init__(self, parent_surface: pygame.Surface, name: str, rect: pygame.Rect, background_color: tuple[int, int, int] = None, border: bool = False, border_color: tuple[int, int, int] = DEFAULT_WIDGET_BORDER_COLOR, font: WidgetFont = None, speed: int = 1, source: Optional[HorizontalTickerWidgetSource] = None) -> None:
        super().__init__(parent_surface = parent_surface, name = name, rect = rect, background_color = background_color, border = border, border_color = border_color)
        if not font:
            raise RuntimeError("Font not set")
        if not source:
            raise RuntimeError("Source not set")
        self.__font = font
        self.__source = source
        self.__text_surface = self.__font.render(f"{source.text} {SEPARATOR} ")
        self.__speed = speed
        self.__x_offset = 0
        self.__y_offset = (self.height - self.__text_surface.get_height()) // 2
        self.__render_required = True

    def refresh(self, force: bool = False) -> bool:
        if self.__source.changed():
            try:
                self.__source.reload()
                self.__text_surface = self.__font.render(f"{self.__source.text} {SEPARATOR} ")
            except Exception as e:
                self._log.error(f"Error updating source: {e}")
                self.__text_surface = self.__font.render(f"SOURCE UPDATE ERROR {SEPARATOR} ")
            self.__x_offset = 0
            self.__render_required = True
        if force or self.__render_required:
            super()._clear()
            text_width = self.__text_surface.get_width()
            num_repeats = (self.width // text_width) + 2
            for i in range(num_repeats):
                x_position = self.__x_offset + i * text_width
                self._blit(self.__text_surface, (x_position, self.__y_offset))
            self.__x_offset -= self.__speed
            if self.__x_offset < -text_width:
                self.__x_offset += text_width
            super()._render()
        return True

    def on_click(self):
        self._log.debug("detected widget click event, forcing refresh")
        self.__x_offset = 0
        self.refresh(True)
