from typing import Optional, Any
from abc import abstractmethod
import pygame


from ..widget import Widget, DEFAULT_WIDGET_BORDER_COLOR
from ..widget_font import WidgetFont, WidgetFontTextAlign

class ChartWidgetHorizontalTextBlock():
    def __init__(self, font: WidgetFont, text_align: WidgetFontTextAlign, text: Optional[str] = None, masked_text: Optional[str] = None, fixed_width: Optional[int] = None):
        self.__font = font
        self.__text = text
        self.__masked_text = masked_text
        self.__text_align = text_align
        self.__fixed_width = fixed_width
        if self.__text_align != WidgetFontTextAlign.LEFT and self.__fixed_width < 1:
            raise ValueError("Invalid fixed width required for center/right text align")

    @property
    def has_static_text(self) -> bool:
        return self.__text is not None

    def render_text(self) -> pygame.surface:
        if self.__text_align == WidgetFontTextAlign.CENTER or self.__text_align == WidgetFontTextAlign.RIGHT:
            return self.__font.render_aligned(text = self.__text, fixed_width = self.__fixed_width, align = self.__text_align)
        else:
            return self.__font.render(text = self.__text)

    def render_masked_text(self, current_value: Any, min_value: Optional[Any] = None, max_value: Optional[Any] = None):
        formatted_text = self.__masked_text.format(current_value = current_value, min_value = min_value, max_value = max_value)
        if self.__text_align == WidgetFontTextAlign.CENTER or self.__text_align == WidgetFontTextAlign.RIGHT:
            return self.__font.render_aligned(text = formatted_text, fixed_width = self.__fixed_width, align = self.__text_align)
        else:
            return self.__font.render(text = formatted_text)


class ChartWidget(Widget):
    def __init__(self, parent_surface: pygame.Surface, name: str, rect: pygame.Rect, background_color: tuple[int, int, int] = None, border: bool = False, border_color: tuple[int, int, int] = DEFAULT_WIDGET_BORDER_COLOR, top_title_block: Optional[ChartWidgetHorizontalTextBlock] = None, bottom_legend_block: Optional[ChartWidgetHorizontalTextBlock] = None) -> None:
        super().__init__(parent_surface = parent_surface, name = name, rect = rect, background_color = background_color, border = border, border_color = border_color)
        self._refresh_required = True
        self._top_title_block = top_title_block
        self._bottom_legend_block = bottom_legend_block

    @abstractmethod
    def refresh(self, force: bool = False) -> bool:
        pass

    def on_click(self):
        self._log.debug("Detected widget click event, doing nothing")
