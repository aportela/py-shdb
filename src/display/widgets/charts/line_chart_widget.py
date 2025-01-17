import pygame
import random

from typing import Optional
from .chart_widget import ChartWidget, ChartWidgetHorizontalTextBlock
from ..widget import DEFAULT_WIDGET_BORDER_COLOR
from ....modules.mqtt.data_sources.mqtt_data_source import MQTTDataSource
from ....modules.queue.queue import QueueMSG

class LineChartWidget(ChartWidget):

    def __init__(self, parent_surface: pygame.Surface, name: str, rect: pygame.Rect, background_color: tuple[int, int, int] = None, border: bool = False, border_color: tuple[int, int, int] = DEFAULT_WIDGET_BORDER_COLOR, top_title_block: Optional[ChartWidgetHorizontalTextBlock] = None, bottom_legend_block: Optional[ChartWidgetHorizontalTextBlock] = None, data_source: MQTTDataSource = None) -> None:
        super().__init__(parent_surface = parent_surface, name = name, rect = rect, background_color = background_color, border = border, border_color = border_color, top_title_block = top_title_block, bottom_legend_block = bottom_legend_block)
        self._refresh_required = True
        self.__data_source = data_source
        self.__min_value = None
        self.__max_value = None
        self.__current_value = None
        self.__tmp_surface = pygame.Surface((self.width, self.height))
        self.__tmp_surface.fill((0, 0, 0))
        self._chart_height = self.height
        self.__top_title_surface = None
        self.__refresh_top_title_surface()
        if self.__top_title_surface is not None:
            self._chart_height -= self.__top_title_surface.get_height()
        self.__bottom_legend_surface = None
        self.__refresh_bottom_legend_surface()
        if self.__bottom_legend_surface is not None:
            self._chart_height -= self.__top_title_surface.get_height()

    def set_data_source(self, data_source: MQTTDataSource):
        self.__data_source = data_source

    def __map_value(self, value, fromLow, fromHigh, toLow, toHigh):
        return (value - fromLow) * (toHigh - toLow) / (fromHigh - fromLow) + toLow

    def __get_value(self) -> bool:
        value = self.__data_source.dequeue()
        if value is not None:
            self.__current_value = value.value
            if (self.__min_value is not None):
                if self.__current_value < self.__min_value:
                    self.__min_value = self.__current_value
            else:
                self.__min_value = self.__current_value
            if (self.__max_value is not None):
                if self.__current_value > self.__max_value:
                    self.__max_value = self.__current_value
            else:
                self.__max_value = self.__current_value
            return True
        else:
            return False

    def __refresh_top_title_surface(self) -> None:
        if self._top_title_block is not None:
            if self._top_title_block.has_static_text:
                self.__top_title_surface = self._top_title_block.render_text()
            else:
                self.__top_title_surface = self._top_title_block.render_masked_text(
                    current_value = self.__current_value if self.__current_value is not None else 0,
                    min_value = self.__min_value if self.__min_value is not None else 0,
                    max_value = self.__max_value if self.__max_value is not None else 0
                )

    def __refresh_bottom_legend_surface(self) -> None:
        if self._bottom_legend_block is not None:
            if self._bottom_legend_block.has_static_text:
                self.__bottom_legend_surface = self._bottom_legend_block.render_text()
            else:
                self.__bottom_legend_surface = self._bottom_legend_block.render_masked_text(
                    current_value = self.__current_value if self.__current_value is not None else 0,
                    min_value = self.__min_value if self.__min_value is not None else 0,
                    max_value = self.__max_value if self.__max_value is not None else 0
                )

    def __render_graph(self, value: int) -> pygame.Surface:
        surface = pygame.Surface((self.width, self.height))
        surface.fill((0, 0, 0))

        if self._title_surface is not None:
            surface.blit(self._title_surface, (0,0))

        start_pos = (4, 4)
        if self._title_surface is not None:
            start_pos = (4, 4 + self._title_surface.get_height() + 4)
        end_pos = (4, self.height - 4)
        pygame.draw.line(surface=surface, color=(255, 255, 255), start_pos=start_pos, end_pos=end_pos, width=2)

        start_pos = (4, self.height - 4)
        end_pos = (self.width - 4, self.height - 4)
        pygame.draw.line(surface=surface, color=(255, 255, 255), start_pos=start_pos, end_pos=end_pos, width=2)

        x = self.__graph_surface.get_width() -1
        y = self.__graph_surface.get_height() -1

        v = int(self.__map_value(value, 0, y, 0, 100))


        pygame.draw.line(surface=self.__graph_surface, color=(0, 0, 0), start_pos=(x, 0), end_pos=(x, y), width=1) # delete with black vertical line
        self.__graph_surface.set_at((x, y - v), (255, 0, 255)) # pixel
        pygame.draw.line(surface=self.__graph_surface, color=(125, 0, 125), start_pos=(x, y - v +1), end_pos=(x, y), width=1) ## line (fill bg)
        surface.blit(source = self.__graph_surface, dest=(6, 6))
        self.__graph_surface.scroll(dx = -1, dy = 0)
        return surface

    def refresh(self, force: bool = False) -> bool:
        self._refresh_required = self.__get_value()
        if force or self._refresh_required:
            super()._clear()
            if self._top_title_block is not None:
                if not self._top_title_block.has_static_text:
                    self.__refresh_top_title_surface()
                super()._blit(self.__top_title_surface, (0, 0))
            if self._bottom_legend_block is not None:
                if not self._bottom_legend_block.has_static_text:
                    self.__refresh_bottom_legend_surface()
                super()._blit(self.__bottom_legend_surface, (0, self.height - self.__bottom_legend_surface.get_height()))

                #self.__tmp_surface.blit(self.__top_title_surface, (0, 0))
            #super()._blit(self.__render_graph(int(value.value)), (0, 0))

            super()._render()
            #self._refresh_required = False
            return True
        else:
            return False

    def on_click(self):
        self._log.debug("Detected widget click event, forcing refresh")
        self.refresh(True)
