import pygame
import random

from .chart_widget import ChartWidget
from ..widget import DEFAULT_WIDGET_BORDER_COLOR
from ....modules.mqtt.data_sources.mqtt_data_source import MQTTDataSource
from ....modules.queue.queue import QueueMSG

class LineChartWidget(ChartWidget):

    def __init__(self, parent_surface: pygame.Surface, name: str, rect: pygame.Rect, background_color: tuple[int, int, int] = None, border: bool = False, border_color: tuple[int, int, int] = DEFAULT_WIDGET_BORDER_COLOR, data_source: MQTTDataSource = None) -> None:
        super().__init__(parent_surface = parent_surface, name = name, rect = rect, background_color = background_color, border = border, border_color = border_color)
        self.__refresh_required = True
        self.__graph_surface = pygame.Surface((self.width - 10, self.height - 10))
        self.__graph_surface.fill((0, 0, 0))
        self.__data_source = data_source

    def set_data_source(self, data_source: MQTTDataSource):
        self.__data_source = data_source

    def __map_value(self, value, fromLow, fromHigh, toLow, toHigh):
        return (value - fromLow) * (toHigh - toLow) / (fromHigh - fromLow) + toLow

    def __render_graph(self, value: int) -> pygame.Surface:
        surface = pygame.Surface((self.width, self.height))
        surface.fill((0, 0, 0))
        start_pos = (4, 4)
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
        value = self.__data_source.dequeue()
        if value is not None:
            if force or self.__refresh_required:
                super()._clear()
                super()._blit(self.__render_graph(int(value.value)), (0, 0))
                super()._render()
                #self.__refresh_required = False
                return True
            else:
                return False
        else:
            return False

    def on_click(self):
        self._log.debug("Detected widget click event, forcing refresh")
        self.refresh(True)
