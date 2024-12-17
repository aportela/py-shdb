import pygame
import os

from .widget import Widget

class ImageWidget(Widget):

    def __init__(self, name: str, x: int , y: int, width: int, height: int, padding: int, surface: pygame.Surface, debug: bool, path: str = None):
        # Initialize the parent class (Widget)
        super().__init__(name=name, surface=surface, debug=debug, x=x, y=y, width=width, height=height, padding=padding)

        self._path = path
        self._render_required = True  # this widget has static image (no changes) so only render on first refresh iteration

        if path is not None:
            if os.path.exists(path):
                self._image = pygame.image.load(path)
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
        else:
            raise ValueError("Image path not set")

    def refresh(self, force: bool = False) -> bool:
        if force or self._render_required:
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
