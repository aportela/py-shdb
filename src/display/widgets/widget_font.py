import pygame

class WidgetFont:
    def __init__(self, family: str = None, file: str = None, size: int = 30, color: tuple = (255, 255, 255),
                 style_bold: bool = False, style_italic: bool = False):
        """Initialize the font with the specified properties."""
        self.__family = family
        self.__file = file
        self.__size = size
        self.__color = color
        self.__style_bold = style_bold
        self.__style_italic = style_italic
        self.__font = self.__initialize_font()

    def __initialize_font(self) -> pygame.font.Font:
        """Initialize the font based on file, family, or default settings."""
        if self.__file:
            try:
                return pygame.font.Font(self.__file, self.__size)
            except Exception as e:
                print(f"Error loading font file '{self.__file}': {e}")
                return pygame.font.Font(None, self.__size)
        elif self.__family:
            return pygame.font.SysFont(self.__family, self.__size, self.__style_bold, self.__style_italic)
        else:
            return pygame.font.Font(None, self.__size)

    def update_font(self, family: str = None, file: str = None, size: int = None, color: tuple = None,
                    style_bold: bool = None, style_italic: bool = None) -> None:
        """Update font properties and reinitialize the font."""
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

    def render(self, text: str) -> pygame.Surface:
        """Render the specified text as a pygame.Surface."""
        return self.__font.render(text, True, self.__color)
