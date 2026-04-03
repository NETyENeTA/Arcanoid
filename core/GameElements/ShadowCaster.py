from core.App import AppConfigs as App, pg

from pygame._sdl2 import Renderer, Texture
import pygame as pg


class ShadowCaster:
    def init_shadow(self):
        # 1. Создаем маску формы ОДИН РАЗ как текстуру
        # Она должна быть белой (255, 255, 255), чтобы потом легко перекрашивать
        mask_surf = pg.Surface(self.hitbox.size, pg.SRCALPHA)
        self.draw_shadow_shape(mask_surf, (255, 255, 255, 255))

        self._shadow_texture = Texture.from_surface(self.render, mask_surf)
        # Включаем возможность менять прозрачность и цвет
        self._shadow_texture.blend_mode = pg.BLENDMODE_BLEND
        # self._shadow_texture.blend_mode = 1

    def cast_shadow(self):
        for light in App.LightS.Lights:
            direction = self.center - light.pos
            dist = direction.magnitude

            if dist > 0:
                # 2. Расчеты параметров (длина и прозрачность)
                shadow_len = max(self.shadow_info.minimal,
                                 min(dist * self.shadow_info.middle,
                                     self.shadow_info.maximal))

                alpha_val = max(0, min(160, 180 - int(dist * 0.3)))

                # 3. МАГИЯ SDL2: Вместо создания новых Surface,
                # мы просто меняем свойства существующей текстуры перед отрисовкой
                self._shadow_texture.color = light.color.rgb  # Красим белую маску в цвет света
                self._shadow_texture.alpha = alpha_val  # Устанавливаем прозрачность

                # 4. Расчет позиции
                offset = direction.normalized * shadow_len
                render_rect = pg.Rect((self.pos + offset).xy, self.hitbox.size)

                # 5. Отрисовка (происходит на видеокарте)
                self.render.blit(self._shadow_texture, render_rect)

