import pygame
import random

from .widget import Widget, DEFAULT_WIDGET_BORDER_COLOR
from .widget_font import WidgetFont
from ..font_awesome_unicode_icons import FontAwesomeUnicodeIcons
from ..font_awesome_icon import FontAwesomeIcon
from ..font_awesome_animated_icon import FontAwesomeAnimationSpeed, FontAwesomeAnimationSpinDirection, FontAwesomeIconBeatEffect, FontAwesomeIconBounceEffect, FontAwesomeIconSpinEffect, FontAwesomeIconFlipEffect, FontAwesomeAnimationFlipAxis, FontAwesomeIconFadeEffect, FontAwesomeIconBeatAndFadeEffect

class WeatherForecastWidget(Widget):

    def __init__(self, surface: pygame.Surface, name: str, x: int , y: int, width: int, height: int, padding: int, background_color: tuple[int, int, int, int] = (0, 0, 0, 0), border: bool = False, border_color: tuple[int, int, int] = DEFAULT_WIDGET_BORDER_COLOR, font: WidgetFont = None, text: str = None) -> None:
        super().__init__(surface = surface, name = name, x = x, y = y, width = width, height = height, padding = padding, background_color = background_color, border = border, border_color = border_color)
        if not font:
            raise RuntimeError("Font not set")
        self.__font = font
        if not text:
            raise RuntimeError("Text not set")
        self.__text = text
        super()._blit(self.__font.render(self.__text))
        self._render_required = True
        self._icon = FontAwesomeIconBeatEffect(surface = self._tmp_surface, x = 10, y = 40, icon = FontAwesomeUnicodeIcons.ICON_CLOUD_BOLT, file= "resources/fonts/fa-solid-900.ttf", size = 50, color = (255,255,255), background_color = background_color, speed = FontAwesomeAnimationSpeed.MEDIUM, use_sprite_cache = False, max_size = 60)

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
        icons1 = [ FontAwesomeUnicodeIcons.ICON_SUN, FontAwesomeUnicodeIcons.ICON_CLOUD, FontAwesomeUnicodeIcons.ICON_CLOUD_RAIN, FontAwesomeUnicodeIcons.ICON_CLOUD_BOLT ]
        icons2 = [ FontAwesomeUnicodeIcons.ICON_WIND, FontAwesomeUnicodeIcons.ICON_WIND, FontAwesomeUnicodeIcons.ICON_WIND, FontAwesomeUnicodeIcons.ICON_WIND ]
        icons3 = [ FontAwesomeUnicodeIcons.ICON_TEMPERATURE_0, FontAwesomeUnicodeIcons.ICON_TEMPERATURE_1, FontAwesomeUnicodeIcons.ICON_TEMPERATURE_2, FontAwesomeUnicodeIcons.ICON_TEMPERATURE_3, FontAwesomeUnicodeIcons.ICON_TEMPERATURE_4 ]
        ic = FontAwesomeIcon(file = "resources/fonts/fa-solid-900.ttf", size = 32, color = (255, 255, 255))
        for i in range(len(hours)):
            super()._blit(self.__font.render(hours[i]), (x, y))
            super()._blit(ic.render(random.choice(icons1), (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))), (x+170, y+8))
            super()._blit(ic.render(random.choice(icons2), (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))), (x+220, y+8))
            super()._blit(ic.render(random.choice(icons3), (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))), (x+270, y+8))
            y+= 60
    def refresh(self, force: bool = False) -> bool:
        icon_refreshed = self._icon.animate(60)
        if not self._render_required:
            self._render_required = icon_refreshed
        if force or self._render_required:
            #super()._clear()
            super()._render()
            self._render_required = False
            return True  # Indicate that the widget was rendered successfully
        else:
            return False  # Return False if the widget doesn't need a refresh

    def on_click(self):
        self._log.debug("detected widget click event, forcing refresh")
        self.refresh(True)
