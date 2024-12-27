from typing import Optional
import pygame
import os

from .widget import Widget, DEFAULT_WIDGET_BORDER_COLOR

class ImageWidget(Widget):

    def __init__(self, parent_surface: pygame.Surface, name: str, rect: pygame.Rect, background_color: tuple[int, int, int] = None, border: bool = False, border_color: tuple[int, int, int] = DEFAULT_WIDGET_BORDER_COLOR, path: Optional[str] = None) -> None:
        super().__init__(parent_surface = parent_surface, name = name, rect = rect, background_color = background_color, border = border, border_color = border_color)
        self.__image = None
        if path is None:
            raise ValueError(f"Image path not set")
        self._log.debug(f"Using local path {path}")
        self.__load(path)
        self._render_required = True

    def __load(self, path: str):
        if os.path.exists(path):
            self.__image = pygame.image.load(path)
            original_width, original_height = self.__image.get_size()
            if original_width > self.width or original_height > self.height:
                scale_factor = min(self.width / original_width, self.height / original_height)
                new_width = int(original_width * scale_factor)
                new_height = int(original_height * scale_factor)
                self._log.debug(f"Rescaling from {original_width}x{original_height} to {new_width}x{new_height}.")
                self.__image = pygame.transform.scale(self.__image, (new_width, new_height))
            self.__image = self.__image.convert()
        else:
            raise ValueError(f"Image {path} not found")

    def refresh(self, force: bool = False) -> bool:
        if force or self._render_required:
            if self.__image is None:
                raise ValueError("No image loaded.")
            self._render_required = False
            super()._clear()
            available_width = self.width
            available_height = self.height
            offset_x = (available_width - self.__image.get_width()) // 2
            offset_y = (available_height - self.__image.get_height()) // 2
            super()._blit(self.__image, (offset_x, offset_y))
            super()._render()
            return True
        else:
            return False

    def on_click(self):
        self._log.debug("detected widget click event, forcing refresh")
        self.refresh(True)
