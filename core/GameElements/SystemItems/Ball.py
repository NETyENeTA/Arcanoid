from pygame._sdl2 import Texture, Renderer

from Libraries.SimplePyGame.Positions import Range
from Libraries.SimplePyGame.SDL2.Draw import draw_dashed_circle
from core.GameElements.Rectangle import pg, Vec2
from Libraries.SimplePyGame.Colors import Colors
from Libraries.SimplePyGame.Color import Color

from core.App import AppConfigs as App


import GameFiles.Configs.WindowApp as WindowApp
from Libraries.Math.Random import randrange_int as rnd, random_from_list as rfl
from core.GameElements.ShadowCaster import ShadowCaster


class Ball(ShadowCaster):


    def __init__(self, pos: Vec2, radius: int, color: Color = Colors.BLACK, is_sticky: bool = False):
        self.radius = radius
        self.diameter = radius * 2


        self.hitbox = pg.Rect(0, 0, self.diameter, self.diameter)
        self.hitbox.center = pos.xy

        self.render: Renderer = App.Screen.render
        self.color = color

        self._direction = Vec2(rnd(-1, 1), -1)

        self.speed = Vec2(4, 4)
        self.movement = Vec2(100, 100)

        self.is_sticky = is_sticky

        self.shadow_info = Range(2, 0.1, 15)

        self.init_shadow()

        # Create Ball
        temp_surf = pg.Surface((self.diameter, self.diameter), pg.SRCALPHA)
        pg.draw.circle(temp_surf, self.color.full, (self.radius, self.radius), self.radius)
        self.texture = Texture.from_surface(self.render, temp_surf)

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

        if self.is_sticky and App.keys()[pg.K_SPACE]:
            self.is_sticky = False
            # self.direction.x = rfl([0, 1])

        if self.pos.x < WindowApp.Left:
            self.direction.reflect_x(False)
            self.direction.normalize()
            self.hitbox.left = WindowApp.Left
            # App.sfx.mode_play("ball hit", App.sfx.Modes.Left)
            App.sfx.pos_play("ball hit", self.pos.x)

        elif self.pos.x > WindowApp.right - self.diameter:
            self.direction.reflect_x(True)
            self.direction.normalize()
            # App.sfx.mode_play("ball hit", App.sfx.Modes.Right)
            App.sfx.pos_play("ball hit", self.pos.x)

        elif self.pos.y < WindowApp.Top:
            self.direction.reflect_y(False)
            self.direction.normalize()
            App.sfx.pos_play("ball hit", self.pos.x)

        if not self.is_sticky:
            self.pos += self.direction * self.speed * self.movement * App.dt

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

    def draw(self):
        self.render.blit(self.texture, self.hitbox)

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