from typing import Optional
import pygame
import os
import hashlib
import requests

from .widget import Widget, DEFAULT_WIDGET_BORDER_COLOR
from ...modules.module_cache import ModuleCache

class ImageWidget(Widget):

    def __init__(self, parent_surface: pygame.Surface, name: str, x: int , y: int, width: int, height: int, background_color: tuple[int, int, int] = None, border: bool = False, border_color: tuple[int, int, int] = DEFAULT_WIDGET_BORDER_COLOR, path: Optional[str] = None, url: Optional[str] = None, cache_path: Optional[str] = None) -> None:
        super().__init__(parent_surface = parent_surface, name = name, x = x, y = y, width = width, height = height, background_color = background_color, border = border, border_color = border_color)
        self.__image = None
        if path is not None:
            self._log.debug(f"Using local path {path}")
            self.__load(path)
        elif url is not None:
            self._log.debug(f"Using remote url {url}")
            cache_file_path = f"{cache_path}/images/{hashlib.sha256(url.encode('utf-8')).hexdigest()[:64]}.image"
            if os.path.exists(cache_file_path):
                self._log.debug(f"Remote url image cache found on {cache_file_path}")
                self.__load(cache_file_path)
            else:
                try:
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    if 'image' not in response.headers['Content-Type']:
                        raise ValueError("The URL does not point to a valid image.")
                    cache = ModuleCache(cache_file_path)
                    if cache.save_bytes(response.content) is False:
                        raise ValueError("Error saving cache of remote image.")
                    else:
                        self.__load(cache_file_path)
                except requests.exceptions.RequestException as e:
                    raise ValueError(f"Error fetching image from URL: {e}")
        else:
            raise ValueError("Image path/url not set")
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
