from typing import Optional
import pygame
from enum import Enum

class WidgetFontTextAlign(Enum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2

    @classmethod
    def from_string(cls, text_align_str: str):
        try:
            return cls[text_align_str.upper()]
        except KeyError:
            raise ValueError(f"Invalid text align: '{text_align_str}'. Use 'left', 'centered' or 'right'.")

class WidgetFont:
    def __init__(self, family: Optional[str] = None, file: Optional[str] = None, size: int = 30, color: tuple[int, int, int] = (255, 255, 255),
                 style_bold: bool = False, style_italic: bool = False) -> None:
        self.__family = family
        self.__file = file
        self.__size = size
        self.__color = color
        self.__style_bold = style_bold
        self.__style_italic = style_italic
        self.__font = self.__initialize_font()

    def __initialize_font(self) -> pygame.font.Font:
        if self.__file:
            try:
                return pygame.font.Font(self.__file, size = self.__size)
            except Exception as e:
                print(f"Error loading font file '{self.__file}': {e}.")
                return pygame.font.Font(name = None, size = self.__size, bold = self.__style_bold, italic = self.__style_italic)
        elif self.__family:
            return pygame.font.SysFont(name = self.__family, size = self.__size, bold = self.__style_bold, italic = self.__style_italic)
        else:
            return pygame.font.Font(None, self.__size)

    def update_font(self, family: Optional[str] = None, file: Optional[str] = None, size: int = None, color: tuple[int, int, int] = None,
                    style_bold: bool = None, style_italic: bool = None) -> None:
        if family is not None:
            self.__family = family
        if file is not None:
            self.__file = file
        if size is not None:
            self.__size = size
        if color is not None:
            self.__color = color
        if style_bold is not None:
            self.__style_bold = style_bold
        if style_italic is not None:
            self.__style_italic = style_italic

        self.__font = self.__initialize_font()

    def render(self, text: str, custom_color: tuple[int, int, int] = None) -> pygame.Surface:
        return self.__font.render(text, True, (custom_color if custom_color else self.__color))

    def render_aligned(self, text: str, fixed_width: int, align: WidgetFontTextAlign, custom_color: tuple[int, int, int] = None) -> pygame.Surface:
        if fixed_width > 0:
            surface = self.__font.render(text, True, (custom_color if custom_color else self.__color))
            if (align == WidgetFontTextAlign.CENTER):
                x_offset = (fixed_width - surface.get_width()) // 2
            elif (align == WidgetFontTextAlign.RIGHT):
                x_offset = (fixed_width - surface.get_width())
            else:
                x_offset = 0
            final_surface = pygame.Surface((fixed_width, surface.get_height()), pygame.SRCALPHA)
            final_surface.blit(surface, (x_offset, 0))
            return final_surface
        else:
            raise ValueError("Invalid fixed width param")
