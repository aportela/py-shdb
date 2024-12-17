import pygame
import os
import hashlib
import requests
from .widget import Widget
from ...modules.module_cache import ModuleCache
from ...utils.logger import Logger

class ImageWidget(Widget):

    def __init__(self, name: str, x: int , y: int, width: int, height: int, padding: int, surface: pygame.Surface, debug: bool, path: str = None, url: str = None, cache_path: str = None):
        # Initialize the parent class (Widget)
        super().__init__(name=name, surface=surface, debug=debug, x=x, y=y, width=width, height=height, padding=padding)

        self.__log = Logger()
        self._path = path
        self._render_required = True  # this widget has static image (no changes) so only render on first refresh iteration
        self._image = None
        if path is not None:
            self.__log.debug(f"Using local path {path}")
            self.__load(path)
        elif url is not None:
            self.__log.debug(f"Using remote url {url}")
            cache_file_path = f"{cache_path}/images/{hashlib.sha256(url.encode('utf-8')).hexdigest()[:64]}.image"
            if os.path.exists(cache_file_path):
                self.__load(cache_file_path)
            else:
                try:
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    if 'image' not in response.headers['Content-Type']:
                        raise ValueError("The URL does not point to a valid image")
                    cache = ModuleCache(cache_file_path)
                    cache.save_bytes(response.content)
                    self.__load(cache_file_path)
                except requests.exceptions.RequestException as e:
                    raise ValueError(f"Error fetching image from URL: {e}")
        else:
            raise ValueError("Image path/url not set")

    def __load(self, path: str):
        if os.path.exists(path):
            self._image = pygame.image.load(path)
            self.__log.debug(self._image)
            original_width, original_height = self._image.get_size()
            # Scale the image to fit the widget size (self._width and self._height)
            if original_width > self._width or original_height > self._height:
                scale_factor = min(self._width / original_width, self._height / original_height)
                new_width = int(original_width * scale_factor)
                new_height = int(original_height * scale_factor)
                self._image = pygame.transform.scale(self._image, (new_width, new_height))

            # Convert the image for optimal blitting (faster performance)
            self._image = self._image.convert()
        else:
            raise ValueError(f"Image {path} not found")

    def refresh(self, force: bool = False) -> bool:
        if force or self._render_required:
            if self._image is None:
                raise ValueError("No image loaded.")
            self._render_required = False
            self._clear()
            # Calculate the available width and height considering the padding
            available_width = self._width - 2 * self._padding
            available_height = self._height - 2 * self._padding
            # Calculate the offsets to center the image within the available space
            offset_x = (available_width - self._image.get_width()) // 2
            offset_y = (available_height - self._image.get_height()) // 2
            self._tmp_surface.blit(self._image, (offset_x, offset_y))
            super()._render()
            return True
        else:
            return False
