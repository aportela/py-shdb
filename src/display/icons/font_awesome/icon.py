from typing import Optional
import os
import pygame

from .icon_list import IconList as FontAwesomeIcon
from ....utils.logger import Logger

class Icon():
    """
    A class to represent and render FontAwesome icons using Pygame.

    This class allows the creation of an icon object with a specific FontAwesome
    font, size, and color. It supports custom icon rendering on Pygame surfaces.
    """

    # A class-level default font path, shared among all instances
    __default_font_path: Optional[str] = None

    def __init__(self, font_path: Optional[str] = None, size: int = 16, color: tuple[int, int, int] = (255, 255, 255)) -> None:
        """
        Initializes an Icon instance with a specific font, size, and color.

        Args:
            font_path (Optional[str]): The path to the FontAwesome font file. If not provided,
                                        it will use the default class-level font path.
            size (int): The size of the icon. Default is 16.
            color (tuple[int, int, int]): The color of the icon as an RGB tuple. Default is white (255, 255, 255).

        Raises:
            ValueError: If the font path is invalid or not set.
        """
        # Check if a custom font path is provided and if it exists, otherwise use the default font path
        if font_path is not None:
            if not os.path.exists(font_path):
                raise ValueError(f"Font awesome external file path {font_path} not found.")
            else:
                self.__font_path = font_path
        elif Icon.__default_font_path is None:
            raise ValueError(f"Font awesome external file path not set.")

        self.__size = size
        self.__color = color
        self.__font = self._load_font()  # Load the font using the provided or default font path

    @staticmethod
    def set_default_font_path(font_path: str) -> None:
        """
        Sets the default font path for all instances of the Icon class.

        This method allows you to globally set the FontAwesome font file path to be used
        by all instances of the Icon class if no specific path is provided.

        Args:
            font_path (str): The path to the FontAwesome font file to be used globally.

        Raises:
            ValueError: If the provided font path does not exist.
        """
        if os.path.exists(font_path):
            Icon.__default_font_path = font_path
            Logger().debug(f"Setting default FontAwesome font file path: {font_path}")
        else:
            raise ValueError(f"Font awesome font file {font_path} not found.")

    def _load_font(self) -> pygame.font.Font:
        """
        Loads the font using the current font path and size.

        This helper method handles the font loading process and raises an error
        if the font cannot be loaded.

        Returns:
            pygame.font.Font: The loaded Pygame font object.

        Raises:
            RuntimeError: If the font file cannot be loaded.
        """
        try:
            return pygame.font.Font(self.__font_path, self.__size)
        except Exception as e:
            raise RuntimeError(f"Failed to load font at {self.__font_path}: {e}")

    def set_size(self, size: int) -> None:
        """
        Changes the size of the icon.

        Args:
            size (int): The new size of the icon.
        """
        self.__size = size
        self.__font = self._load_font()  # Reload the font with the new size

    def set_color(self, color: tuple[int, int, int]) -> None:
        """
        Changes the color of the icon.

        Args:
            color (tuple[int, int, int]): The new color for the icon as an RGB tuple.
        """
        self.__color = color

    def render(self, icon: FontAwesomeIcon, custom_color: Optional[tuple[int, int, int]] = None) -> pygame.Surface:
        """
        Renders the specified FontAwesome icon as a Pygame Surface.

        Args:
            icon (FontAwesomeIcon): The icon to render. This should be a member of the FontAwesomeIcon list.
            custom_color (Optional[tuple[int, int, int]]): An optional color for the icon. If not provided,
                                                           the icon will be rendered with the default color.

        Returns:
            pygame.Surface: A Pygame surface containing the rendered icon.

        Notes:
            If no `custom_color` is provided, the icon will be rendered with the color
            set during initialization or updated using `set_color`.
        """
        color = custom_color if custom_color else self.__color  # Use custom color if provided
        return self.__font.render(icon, True, color)  # Render the icon with the chosen color
