from typing import Optional
import pygame

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

    def render_aligned(self, text: str, custom_color: tuple[int, int, int] = None, fixed_width: int = 0, align: str = None) -> pygame.Surface:
        surface = self.__font.render(text, True, (custom_color if custom_color else self.__color))
        if (align == "center"):
            x_offset = (fixed_width - surface.get_width()) // 2
        elif (align == "right"):
            x_offset = (fixed_width - surface.get_width())
        elif (align == "left"):
            x_offset = 0
        else:
            raise ValueError(f"Invalid align param: {align} on WidgetFont::render_aligned() method")
        final_surface = pygame.Surface((fixed_width, surface.get_height()))
        final_surface.fill((0,0,0))
        final_surface.blit(surface, (x_offset, 0))
        return final_surface
