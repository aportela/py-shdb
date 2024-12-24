from typing import Optional
import pygame
import random

from .widget import Widget, DEFAULT_WIDGET_BORDER_COLOR
from .widget_font import WidgetFont
from ..icons.font_awesome.icon_list import IconList as FontAwesomeIcons
from ..icons.font_awesome.icon import Icon as FontAwesomeIcon

from ..icons.font_awesome.enums import AnimationSpeed as FontAwesomeAnimationSpeed
from ..icons.font_awesome.animations.beat import FontAwesomeIconBeatEffect

class WeatherForecastWidget(Widget):

    def __init__(self, parent_surface: pygame.Surface, name: str, rect: pygame.Rect, background_color: tuple[int, int, int] = None, border: bool = False, border_color: tuple[int, int, int] = DEFAULT_WIDGET_BORDER_COLOR, font: WidgetFont = None, text: Optional[str] = None) -> None:
        super().__init__(parent_surface = parent_surface, name = name, rect = rect, background_color = background_color, border = border, border_color = border_color)
        if not font:
            raise RuntimeError("Font not set")
        self.__font = font
        if not text:
            raise RuntimeError("Text not set")
        self.__text = text
        self._icon = FontAwesomeIconBeatEffect(parent_surface = self.parent_surface,
                                               x = 10, y = 40,
                                               icon = FontAwesomeIcons.ICON_CLOUD_BOLT,
                                               font_path= "resources/fonts/fa-solid-900.ttf",
                                               size = 50,
                                               color = (255,255,255),
                                               speed = FontAwesomeAnimationSpeed.MEDIUM,
                                               max_size = 60
        )

    def __blit_defaults(self):
        super()._blit(self.__font.render(self.__text))
        self._render_required = True

        self.__font.update_font(size = 32)
        super()._blit(self.__font.render("NOW"), (80, 52))
        self.__font.update_font(size = 14)
        super()._blit(self.__font.render("Rain probability : 50%"), (160, 50))
        super()._blit(self.__font.render("Temperature      : 11º"), (160, 70))
        super()._blit(self.__font.render("Wind speed       : 7Km/h"), (160, 90))

        self.__font.update_font(size = 50)
        hours = ["16:00", "17:00", "18:00", "19:00", "20:00", "21:00" ]
        x = 4
        y = 110
        icons1 = [ FontAwesomeIcons.ICON_SUN, FontAwesomeIcons.ICON_CLOUD, FontAwesomeIcons.ICON_CLOUD_RAIN, FontAwesomeIcons.ICON_CLOUD_BOLT ]
        icons2 = [ FontAwesomeIcons.ICON_WIND, FontAwesomeIcons.ICON_WIND, FontAwesomeIcons.ICON_WIND, FontAwesomeIcons.ICON_WIND ]
        icons3 = [ FontAwesomeIcons.ICON_TEMPERATURE_0, FontAwesomeIcons.ICON_TEMPERATURE_1, FontAwesomeIcons.ICON_TEMPERATURE_2, FontAwesomeIcons.ICON_TEMPERATURE_3, FontAwesomeIcons.ICON_TEMPERATURE_4 ]
        ic = FontAwesomeIcon(font_file_path = "resources/fonts/fa-solid-900.ttf", size = 32, color = (255, 255, 255))
        for i in range(len(hours)):
            super()._blit(self.__font.render(hours[i]), (x, y))
            super()._blit(ic.render(random.choice(icons1), (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))), (x+170, y+8))
            super()._blit(ic.render(random.choice(icons2), (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))), (x+220, y+8))
            super()._blit(ic.render(random.choice(icons3), (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))), (x+270, y+8))
            y+= 60

    def refresh(self, force: bool = False) -> bool:
        icon_surface = self._icon.render()
        self._render_required = icon_surface is not None
        if force or self._render_required:
            super()._clear()
            #self.__blit_defaults()
            #self._icon.clear_prev()
            super()._blit(icon_surface)
            #self._icon.update_1()
            super()._render()
            self._render_required = False
            return True  # Indicate that the widget was rendered successfully
        else:
            return False  # Return False if the widget doesn't need a refresh

    def on_click(self):
        self._log.debug("detected widget click event, forcing refresh")
        self.refresh(True)
