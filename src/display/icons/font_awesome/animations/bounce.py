from typing import Optional
import pygame

from ..animated_icon import FontAwesomeIconBaseEffect
from ..icon_list import IconList as FontAwesomeIcons
from ..enums import AnimationType as FontAwesomeAnimationType, AnimationSpeed as FontAwesomeAnimationSpeed

class FontAwesomeIconBounceEffect(FontAwesomeIconBaseEffect):
    def __init__(self, parent_surface: pygame.Surface, x: int, y: int, icon: FontAwesomeIcons, font_file_path: Optional[str] = None, size: int = 16, color: tuple[int, int, int] = (255, 255, 255), background_color: tuple[int, int, int] = None, speed: FontAwesomeAnimationSpeed = FontAwesomeAnimationSpeed.MEDIUM) -> None:
        super().__init__(parent_surface = parent_surface, x = x, y = y, icon = icon, font_file_path = font_file_path, size = size, color = color, background_color = background_color, speed = speed)
        self._animation_type = FontAwesomeAnimationType.BOUNCE
        self.__icon_surface = super().render(self._icon, self._color)
        total_height = self.__icon_surface.get_height() + (self.__icon_surface.get_height() // 2)
        super()._create_temporal_surface((self.__icon_surface.get_width(), total_height))
        self.__x = 0
        self.__y = 0
        self.__min_y = 0
        self.__max_y = total_height - self.__icon_surface.get_height()
        self.__falling = True
        # TODO
        diff = self.__max_y - self.__min_y
        botes = 4
        #print (f"Diff: {diff}")
        #print (f"Botes: {botes}")
        total = self.__calc_distance(diff, diff / botes, speed)
        #print(f"Total {total}")
        self._set_animation_total_frames(total)
        self.__animation_unit = self._frame_skip

    def __calc_distance(self, h_inicial, d, speed: FontAwesomeAnimationSpeed):
        total_distancia = 0
        altura_actual = h_inicial

        while altura_actual > 0:
            # Agrega subida y caída
            total_distancia += 2 * altura_actual
            # Reduce la altura para el próximo rebote
            if (speed ==  FontAwesomeAnimationSpeed.FAST):
                altura_actual -= d * 0.5
            elif (speed ==  FontAwesomeAnimationSpeed.MEDIUM):
                altura_actual -= d * 2
            elif (speed ==  FontAwesomeAnimationSpeed.SLOW):
                altura_actual -= d * 3

        # Resta el último "bote" que no sube
        total_distancia -= altura_actual
        return total_distancia

    def _animate(self) -> bool:
        if self.__min_y < self.__max_y:
            if self.__falling:
                if self.__y < self.__max_y:
                    self.__y += self._frame_skip
                else:
                    self.__falling = False
                    self.__min_y += self._frame_skip
                    #self.__animation_unit += 1
            else:
                if self.__y > self.__min_y:
                    self.__y -= self._frame_skip
                else:
                    self.__falling = True
            self._blit(self.__icon_surface, (self.__x, self.__y))
            return True
        else:
            return False
