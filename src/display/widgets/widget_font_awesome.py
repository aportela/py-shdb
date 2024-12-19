from enum import Enum
import pygame
from .widget_font import WidgetFont

class FontAwesomeIcon(Enum):
    COG = "\uf013"

class FontAwesomeEffect(Enum):
    NONE = 0,
    ROTATE = 1

class FontAwesomeEffectSpeed(Enum):
    SLOW = 0,
    MEDIUM = 1,
    FAST = 2

class WidgetFontAwesome(WidgetFont):
    def __init__(self, file: str = None, size: int = 30, color: tuple = (255, 255, 255)) -> None:
        # Initialize the parent class (WidgetFont) with the provided parameters
        super().__init__(file = file, size = size, color = color, style_bold = False, style_italic = False)

    def render(self, icon: FontAwesomeIcon, effect: FontAwesomeEffect = FontAwesomeEffect.NONE, effect_speed: FontAwesomeEffectSpeed = FontAwesomeEffectSpeed.MEDIUM, custom_color: tuple = None) -> pygame.Surface:
        """Render the specified text as a pygame.Surface."""
        if (effect != FontAwesomeEffect.NONE):
            return self.__font.render(icon, True, custom_color or self.__color)
        else:
            return self.__font.render(icon, True, custom_color or self.__color)
