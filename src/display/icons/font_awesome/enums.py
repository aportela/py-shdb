from enum import Enum

# SIMULATE animations of https://docs.fontawesome.com/web/style/animate#_top
class AnimationType(Enum):
    NONE = 0
    BEAT = 1
    FADE = 2
    BEAT_AND_FADE = 3
    BOUNCE = 4
    HORIZONTAL_FLIP = 5
    VERTICAL_FLIP = 6
    SHAKE = 7
    SPIN_CLOCKWISE = 8
    SPIN_COUNTERCLOCKWISE = 9

class AnimationSpeed(Enum):
    SLOW = 1
    MEDIUM = 4
    FAST = 8

class FlipAnimationAxis(Enum):
    HORIZONTAL = 1
    VERTICAL = 2

class SpinAnimationDirection(Enum):
    CLOCKWISE = 1
    COUNTERCLOCKWISE = 2
