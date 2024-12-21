import pygame

class FPS:
    """
    A class to manage framerate in a pygame application using static methods.
    """

    __clock = pygame.time.Clock()
    __default_fps = 60

    @staticmethod
    def get_current_fps() -> int:
        """
        Retrieves the current FPS calculated by pygame.

        Returns:
            float: The current framerate.
        """
        return int(FPS.__clock.get_fps())

    @staticmethod
    def tick(max_framerate: int = None) -> None:
        """
        Limits the framerate to a specified maximum.

        Args:
            max_framerate (int): The maximum FPS to limit. Defaults to the predefined value.

        Raises:
            ValueError: If max_framerate is not a positive integer.
        """
        if max_framerate is None:
            max_framerate = FPS.__default_fps
        if not isinstance(max_framerate, int) or max_framerate <= 0:
            raise ValueError("max_framerate must be a positive integer.")
        FPS.__clock.tick(max_framerate)

    @staticmethod
    def get_time() -> float:
        """
        Retrieves the time in milliseconds elapsed between the last frame and the current one.

        Returns:
            float: Time elapsed in milliseconds.
        """
        return FPS.__clock.get_time()

    @staticmethod
    def set_default_fps(fps: int) -> None:
        """
        Updates the default FPS limit.

        Args:
            fps (int): The new default FPS limit.

        Raises:
            ValueError: If fps is not a positive integer.
        """
        if not isinstance(fps, int) or fps <= 0:
            raise ValueError("The default FPS must be a positive integer.")
        FPS.__default_fps = fps
