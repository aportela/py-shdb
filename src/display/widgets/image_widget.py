import pygame
import os
import hashlib
import requests
from .widget import Widget
from ...modules.module_cache import ModuleCache

class ImageWidget(Widget):

    def __init__(self, name: str, x: int , y: int, width: int, height: int, padding: int, background_color: tuple[int, int, int, int] = (0, 0, 0, 0), border: bool = False, surface: pygame.Surface = None, path: str = None, url: str = None, cache_path: str = None):
        # Initialize the parent class (Widget) with the provided parameters
        super().__init__(name = name, x = x, y = y, width = width, height = height, padding = padding, background_color = background_color, border = border, surface = surface)

        # Set the path for the image and initialize the image variable
        self._path = path
        self._image = None

        # If the image path is provided, load the image from local storage
        if path is not None:
            self._log.debug(f"Using local path {path}")
            self.__load(path)

        # If a URL is provided, attempt to load the image from the remote URL
        elif url is not None:
            self._log.debug(f"Using remote url {url}")
            # Generate a unique cache file name using the URL hash
            cache_file_path = f"{cache_path}/images/{hashlib.sha256(url.encode('utf-8')).hexdigest()[:64]}.image"

            # If the image is already cached, load it from the cache
            if os.path.exists(cache_file_path):
                self.__load(cache_file_path)

            # Otherwise, download the image and cache it
            else:
                try:
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()  # Check if the request was successful
                    # Check if the response is an image
                    if 'image' not in response.headers['Content-Type']:
                        raise ValueError("The URL does not point to a valid image")

                    # Cache the image and load it
                    cache = ModuleCache(cache_file_path)
                    cache.save_bytes(response.content)
                    self.__load(cache_file_path)

                # Catch any exceptions during the image fetching process
                except requests.exceptions.RequestException as e:
                    raise ValueError(f"Error fetching image from URL: {e}")

        # If neither path nor URL is provided, raise an error
        else:
            raise ValueError("Image path/url not set")

        # Mark the widget as requiring rendering only once (for static images)
        self._render_required = True  # this widget has static image (no changes) so only render on first refresh iteration

    def __load(self, path: str):
        # Check if the image file exists at the provided path
        if os.path.exists(path):
            # Load the image using Pygame
            self._image = pygame.image.load(path)
            original_width, original_height = self._image.get_size()

            # If the image is larger than the widget, scale it to fit within the widget's size
            if original_width > self._width or original_height > self._height:
                scale_factor = min(self._width / original_width, self._height / original_height)
                new_width = int(original_width * scale_factor)
                new_height = int(original_height * scale_factor)
                self._log.debug(f"Rescaling from {original_width}x{original_height} to {new_width}x{new_height}")
                self._image = pygame.transform.scale(self._image, (new_width, new_height))

            # Convert the image for faster blitting performance
            self._image = self._image.convert()
        else:
            # Raise an error if the image file is not found
            raise ValueError(f"Image {path} not found")

    def refresh(self, force: bool = False) -> bool:
        # Only refresh the image if required or forced
        if force or self._render_required:
            # Check if an image has been loaded
            if self._image is None:
                raise ValueError("No image loaded.")

            self._render_required = False
            self._clear()  # Clear the widget's surface before redrawing

            # Calculate the available width and height for the image, considering padding
            available_width = self._width - 2 * self._padding
            available_height = self._height - 2 * self._padding

            # Calculate the offsets to center the image within the available space
            offset_x = (available_width - self._image.get_width()) // 2
            offset_y = (available_height - self._image.get_height()) // 2

            # Blit the image onto the temporary surface
            self._blit(self._image, (offset_x, offset_y))

            # Call the parent class's render method to render the image on the surface
            super()._render()
            return True
        else:
            return False
