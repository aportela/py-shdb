from typing import Optional
import pygame

from .widget import Widget, DEFAULT_WIDGET_BORDER_COLOR
from .widget_font import WidgetFont
from ..icons.font_awesome.icon_list import IconList

class ListWidgetHeader():
    def __init__(self, font: WidgetFont, text: str):
        self.__font = font
        self.__text = text

    @property
    def text (self) -> str:
        return self.__text

    def render(self) -> pygame.surface:
        return self.__font.render(self.__text)


class ListWidgetItem():
    def __init__(self, text: str, icon: Optional[IconList] = None):
        self.__text = text
        self.__icon = icon

    @property
    def text (self) -> str:
        return self.__text

    @property
    def icon (self) -> Optional[IconList]:
        return self.__icon

class ListWidgetBody():
    def __init__(self, font: WidgetFont, items: list[ListWidgetItem]):
        self.__font = font
        self.__items = items

    def clear_items(self) -> None:
        self.__items.clear()

    def add_item(self, item: ListWidgetItem) -> None:
        self.__items.append(item)

    @property
    def item_count(self) -> int:
        return len(self.__items)

    def render_item(self, item_index) -> pygame.surface:
        if item_index >= 0 and item_index < self.item_count:
            return self.__font.render(self.__items[item_index].text)
        else:
            print (item_index)
            print (self.item_count)

            #raise ValueError("Item out of bounds")
            return pygame.Surface((1,1))

    def items(self) -> list[ListWidgetItem]:
        return self.__items


class ListWidget(Widget):

    def __init__(self, parent_surface: pygame.Surface, name: str, rect: pygame.Rect, background_color: tuple[int, int, int] = None, border: bool = False, border_color: tuple[int, int, int] = DEFAULT_WIDGET_BORDER_COLOR, header: Optional[ListWidgetHeader] = None, body: Optional[ListWidgetBody] = None) -> None:
        super().__init__(parent_surface = parent_surface, name = name, rect = rect, background_color = background_color, border = border, border_color = border_color)
        """
        if not font:
            raise RuntimeError("Font not set")
        self.__font = font
        self.__text = None
        """
        self.__header = header
        self.__header_surface = self.__header.render()
        self.__body = body
        self.__refresh_required = True
        self.__show_separator = True

    def refresh(self, force: bool = False) -> bool:
        if force or self.__refresh_required:
            super()._clear()
            super()._blit(self.__header_surface, (0, 0))
            y = self.__header_surface.get_height() + 8
            if self.__show_separator:
                line_surface = pygame.Surface((self.width, 1))
                line_surface.fill((255, 255, 255))
                super()._blit(line_surface, (0, y))
                y += 8

            for i in range(self.__body.item_count):
                item_surface = self.__body.render_item(i)
                super()._blit(item_surface, (0, y))
                y += item_surface.get_height() + 8
            super()._render()
            self.__refresh_required = False
            return True
        else:
            return False

    def on_click(self):
        self._log.debug("Detected widget click event, forcing refresh")
        self.refresh(True)
