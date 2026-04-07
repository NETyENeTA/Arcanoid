from Libraries.Python.Command import Command
from Libraries.SimplePyGame.Color import Color
from Libraries.SimplePyGame.Colors import Colors
from Libraries.SimplePyGame.SDL2.UI.Rectangle import Rectangle, pg
from pygame._sdl2.video import Texture
from math import sin

from Libraries.SimplePyGame.Positions import Vec2, Range
from core.GameElements.ShadowCaster import ShadowCaster
from core.GameElements.Systems.Items.Bonus.BonusColors import BonusColors

from core.App import AppConfigs as App


class Bonus(Rectangle, ShadowCaster):
    _Texture_Cashe = {}

    def __init__(self, size, color: BonusColors, pos=Vec2.Zero, command: Command = None, render=None):
        super().__init__(pos, size, None, render)
        self.hitbox.center = pos.xy

        self.Command = command
        self.color = color

        self.fallSpeed = 2
        self.fallMovement = 100

        # 1. Генерируем текстуру ОДИН РАЗ при создании объекта
        # self.texture = self._create_base_texture()
        self.texture = self._get_cashed_texture(self.color.default)

        self.shadow_info = Range(2, 0.1, 30)
        self.init_shadow()

    def draw_shadow_shape(self, surf, color):
        # Рисуем прямоугольник во весь размер поверхности
        pg.draw.rect(surf, color, (0, 0, *self.hitbox.size), border_radius=4)

    def _get_cashed_texture(self, color: Color):

        if color.rgba not in self._Texture_Cashe:
            self._Texture_Cashe[color.rgba] = self._create_base_texture()

        return self._Texture_Cashe[color.rgba]

    def _create_base_texture(self):
        # Создаем поверхность, рисуем на ней бонус и символ
        surf = pg.Surface((self.hitbox.w, self.hitbox.h), pg.SRCALPHA)
        pg.draw.rect(surf, self.color.default.rgba, (0, 0, self.hitbox.w, self.hitbox.h), border_radius=5)
        # Можно сразу отрисовать букву W/F здесь
        return Texture.from_surface(self.render, surf)

    def update(self):
        self.hitbox.y += self.fallSpeed * self.fallMovement * App.dt

    def draw(self):
        time_ms = pg.time.get_ticks()
        raw_sin = sin(time_ms / 250)
        scale_factor = abs(raw_sin)

        # 2. Считаем новую ширину
        new_w = max(1, int(scale_factor * self.hitbox.w))

        # 3. Создаем целевой прямоугольник для отрисовки
        # Он сжат, но текстура та же самая! Видеокарта сама её сузит.
        dest_rect = pg.Rect(0, 0, new_w, self.hitbox.h)
        dest_rect.center = self.hitbox.center

        # Сохраняем текущий цвет
        original_color = self.texture.color

        # Эффект затемнения задника через свойство текстуры (очень быстро)
        if raw_sin < 0:
            self.texture.color = pg.Color(150, 150, 150)  # Затемняем всю текстуру
        else:
            self.texture.color = pg.Color(255, 255, 255)  # Возвращаем яркость

        # 4. Рендерим готовую текстуру с новым размером
        self.render.blit(self.texture, dest_rect)
        # Возвращаем текущий цвет
        self.texture.color = original_color
