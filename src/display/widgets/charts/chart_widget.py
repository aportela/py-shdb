from abc import abstractmethod
import pygame

from ..widget import Widget, DEFAULT_WIDGET_BORDER_COLOR
from ..widget_font import WidgetFont

class CharWidgetConfiguration():
    def __init__(self, title: str = None):
        self.title = {
            "visible": False,
            "font": None,
            "text": None,
            "align": "center",
            "masked_text": None
        }
        self.legend = {
            "visible": False,
            "font": None,
            "text": None,
            "align": "center",
            "masked_text": None
        }

class ChartWidget(Widget):

    def __init__(self, parent_surface: pygame.Surface, name: str, rect: pygame.Rect, background_color: tuple[int, int, int] = None, border: bool = False, border_color: tuple[int, int, int] = DEFAULT_WIDGET_BORDER_COLOR, config: CharWidgetConfiguration = None) -> None:
        super().__init__(parent_surface = parent_surface, name = name, rect = rect, background_color = background_color, border = border, border_color = border_color)
        self._refresh_required = True
        self._config = config
        self._chart_width = self.width - 10
        self._chart_height = self.height - 10
        self._title_surface = None
        self._legend_surface = None
        if self._config.title is not None and self._config.title["visible"]:
            if self._config.title["font"] is not None and isinstance(self._config.title["font"], WidgetFont):
                self._title_surface = self._config.title["font"].render_aligned(text = self._config.title["text"], fixed_width = self.width, align = "center")
                self._chart_height -= self._title_surface.get_height() - 4
        if self._config.legend is not None and self._config.legend["visible"]:
            if self._config.legend["font"] is not None and isinstance(self._config.legend["font"], WidgetFont):
                self._legend_surface = self._config.legend["font"].render_aligned(text = self._config.legend["text"], fixed_width = self.width, align = "center")
                self._chart_height -= self._legend_surface.get_height() - 4

    @abstractmethod
    def refresh(self, force: bool = False) -> bool:
        pass

    def on_click(self):
        self._log.debug("Detected widget click event, forcing refresh")
        self.refresh(True)
