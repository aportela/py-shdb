import pygame

class WidgetFont:
    """
    A class that encapsulates font properties to render text in Pygame
    with custom styles. It supports both system fonts and custom TTF fonts.

    Attributes:
        font_family (str): The font family (e.g., 'Arial') or None if using a TTF file.
        font_size (int): The font size.
        font_color (tuple): The font color in RGB format (r, g, b).
        font_style_bold (bool): Whether the font is bold.
        font_style_italic (bool): Whether the font is italic.
        font_file (str): The file path to a TTF file, or None to use a system font.
    """

    def __init__(self, font_family: str = None, font_size: int = 30, font_color: tuple = (255, 255, 255),
                 font_style_bold: bool = False, font_style_italic: bool = False,
                 font_file: str = None):
        """
        Initializes the attributes and creates the Pygame font object based on system font or a custom TTF file.
        """
        self.font_family = font_family
        self.font_size = font_size
        self.font_color = font_color
        self.font_style_bold = font_style_bold
        self.font_style_italic = font_style_italic
        self.font_file = font_file

        # Choose the font creation method based on whether a TTF file is provided
        self._update_font()

    @property
    def color(self) -> str:
        return self.font_color

    def _update_font(self):
        """
        Updates the Pygame font object with the current attributes,
        either from a system font or a TTF file.
        """
        if self.font_file:
            # Use custom TTF file if provided
            try:
                self.font = pygame.font.Font(self.font_file, self.font_size)
            except Exception as e:
                print(f"Error loading font file '{self.font_file}': {e}")
                self.font = pygame.font.SysFont(self.font_family, self.font_size, bold=self.font_style_bold,
                                                italic=self.font_style_italic)
        else:
            # Use system font
            self.font = pygame.font.SysFont(self.font_family, self.font_size, bold=self.font_style_bold,
                                           italic=self.font_style_italic)

    def render(self, text: str) -> pygame.Surface:
        """
        Renders the text with the current font styles.

        Args:
            text (str): The text to render.

        Returns:
            pygame.Surface: The surface containing the rendered text.
        """
        return self.font.render(text, True, self.font_color)

    def update_font(self, font_family=None, font_size=None, font_color=None,
                    font_style_bold=None, font_style_italic=None,
                    font_file=None):
        """
        Allows updating any of the font properties, including the option to change between a system font
        and a TTF file.

        Args:
            font_family (str): New font family (used only if no TTF file is provided).
            font_size (int): New font size.
            font_color (tuple): New font color.
            font_style_bold (bool): New value for the bold style.
            font_style_italic (bool): New value for the italic style.
            font_file (str): New file path to a TTF file (or None to use system font).
        """
        if font_family:
            self.font_family = font_family
        if font_size:
            self.font_size = font_size
        if font_color:
            self.font_color = font_color
        if font_style_bold is not None:
            self.font_style_bold = font_style_bold
        if font_style_italic is not None:
            self.font_style_italic = font_style_italic
        if font_file:
            self.font_file = font_file

        self._update_font()  # Update the font with the new values
