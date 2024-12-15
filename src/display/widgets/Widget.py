class Widget:
    def __init__(self):
        self._width = 0
        self._height = 0
        self._xOffset = 0
        self._yOffset = 0
        self._padding = 0
        self._xOffsetWithPadding = 0
        self._yOffsetWithPadding = 0

    def refresh(self, force: bool = False) -> bool:
        return True