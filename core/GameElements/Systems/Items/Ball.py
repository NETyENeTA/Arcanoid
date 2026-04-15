from pygame._sdl2 import Texture, Renderer

from Libraries.SimplePyGame.Positions import Range
from Libraries.SimplePyGame.SDL2.Draw import draw_dashed_circle
from Libraries.SimplePyGame.SDL2.UI.Rectangle import pg, Vec2
from Libraries.SimplePyGame.Colors import Colors
from Libraries.SimplePyGame.Color import Color

from core.App import AppConfigs as App


import GameFiles.Configs.WindowApp as WindowApp
from Libraries.Math.Random import choice
from core.GameElements.ShadowCaster import ShadowCaster
from math import degrees, atan2, cos, sin


class Ball(ShadowCaster):

    SURFACE: pg.Surface = None
    TEXTURE: Texture = None

    def __init__(self, pos: Vec2, radius: int, color: Color = Colors.BLACK, is_sticky: bool = False):
        self.radius = radius
        self.diameter = radius * 2


        self.hitbox = pg.Rect(0, 0, self.diameter, self.diameter)
        self.hitbox.center = pos.xy if isinstance(pos, Vec2) else pos

        self.render: Renderer = App.Screen.render
        self.color = color

        self._direction = Vec2.Zero if is_sticky else Vec2(choice(-1, 1), -1)

        self.speed = Vec2(4, 4)
        self.movement = Vec2(100, 100)

        self.is_sticky = is_sticky

        self.shadow_info = Range(2, 0.1, 15)

        self.init_shadow()

        # Create Ball
        if Ball.SURFACE is None:
            temp_surf = pg.Surface((self.diameter, self.diameter), pg.SRCALPHA)
            pg.draw.circle(temp_surf, self.color.full, (self.radius, self.radius), self.radius)
            Ball.SURFACE = temp_surf

        if Ball.TEXTURE is None:
            # temp_surf = pg.Surface((self.diameter, self.diameter), pg.SRCALPHA)
            # pg.draw.circle(temp_surf, self.color.full, (self.radius, self.radius), self.radius)
            Ball.TEXTURE = Texture.from_surface(self.render, Ball.SURFACE)

    def draw_shadow_shape(self, surf, color):
        # Рисуем круг в центре поверхности
        pg.draw.circle(surf, color, (self.radius, self.radius), self.radius)

    @property
    def pos(self) -> Vec2:
        return Vec2(self.hitbox.topleft)

    @pos.setter
    def pos(self, pos: Vec2):
        self.hitbox.topleft = pos.xy


    def update(self):

        if self.is_sticky and App.realSpacePressed:
            self.is_sticky = False
            App.realSpacePressed = False
            self._direction = Vec2(choice(-1, 1), -1)
            return

        if self.pos.x < WindowApp.Left:
            self.direction.reflect_x(False)
            # self.direction.normalize()
            self.hitbox.left = WindowApp.Left
            # App.sfx.mode_play("ball hit", App.sfx.Modes.Left)
            App.sfx.pos_play("ball hit", self.pos.x)

        elif self.pos.x > WindowApp.right - self.diameter:
            self.direction.reflect_x(True)
            # self.direction.normalize()
            # App.sfx.mode_play("ball hit", App.sfx.Modes.Right)
            App.sfx.pos_play("ball hit", self.pos.x)

        elif self.pos.y < WindowApp.Top:
            self.direction.reflect_y(False)
            # self.direction.normalize()
            App.sfx.pos_play("ball hit", self.pos.x)

        self.pos += self.calculated_speed * App.dt

    @property
    def center(self) -> Vec2:
        return Vec2(self.hitbox.center)

    @property
    def direction(self) -> Vec2:
        return self._direction

    @direction.setter
    def direction(self, direction: Vec2):
        self._direction = direction
        self._direction.normalize()

    @property
    def calculated_speed(self) -> Vec2:
        return self._direction * self.speed * self.movement

    def draw(self):

        # 1. Рассчитываем динамический размер (Squash & Stretch)
        stretch_factor = 0.1
        speed_mag = (abs(self.speed.x * self.direction.x) + abs(self.speed.y * self.direction.y)) / 2

        # Целевые размеры
        width = int(self.diameter + (speed_mag * stretch_factor * 4))
        height = int(self.diameter - (speed_mag * stretch_factor * 4))

        # Ограничение, чтобы не схлопнулся
        width = max(10, width)
        height = max(5, height)

        # 2. Создаем временный Surface для манипуляций
        # Берем оригинальную текстуру (если она есть) или создаем круг
        # ВАЖНО: Мы работаем с Surface, а не с Texture напрямую
        # temp_surf = pg.Surface((self.diameter, self.diameter), pg.SRCALPHA)
        temp_surf = Ball.SURFACE

        # Рисуем шарик на Surface (или используем self.source_surface, если ты ее сохранил)
        # pg.draw.circle(temp_surf, self.color.rgb, (self.diameter // 2, self.diameter // 2), self.radius)

        # 3. Масштабируем (Squash & Stretch)
        temp_surf = pg.transform.scale(temp_surf, (width, height))

        # 4. Поворачиваем по направлению движения
        angle = -degrees(atan2(self.direction.y, self.direction.x))
        rotated_surf = pg.transform.rotate(temp_surf, angle)

        # 5. КОНВЕРТИРУЕМ В ТЕКСТУРУ (самая тяжелая часть, но необходимая для Renderer)
        ball_texture = Texture.from_surface(self.render, rotated_surf)

        # 6. Отрисовываем
        render_rect = rotated_surf.get_rect()
        render_rect.center = self.hitbox.center
        # render_rect.size = (width, height)

        self.render.blit(ball_texture, render_rect)

    def old_draw(self):
        self.render.blit(Ball.TEXTURE, self.hitbox)

    def debug_draw(self):
        self.render.draw_rect(self.hitbox)

    def draw_dashed(self):
        draw_dashed_circle(
            self.render,
            center=self.center,
            radius=self.radius,
            color=self.color.rgba,
            dash_len=5,
            gap_len=10,
            speed=60  # Скорость вращения
        )

    def __str__(self):
        return f"Ball at {self.pos}"

    def __repr__(self):
        return f"{self.pos.xy}"