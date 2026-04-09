from Libraries.Animations.Functions.Lerp import lerp
from Libraries.SimplePyGame.Colors import Colors
from Libraries.SimplePyGame.Positions import Vec2
from Libraries.SimplePyGame.UI.Mouse import Mouse
from Text.Text import Text

from core.GameElements.Systems.Items.Block import Block, pg
from core.App import AppConfigs as App

import GameFiles.Settings.Player as PlayerSettings
import GameFiles.Configs.WindowApp as WindowConfigs

from Libraries.SimplePyGame.SDL2.Draw import draw_circular_dashed_rect as draw_circular


class Paddle(Block):
    class Heart:
        W, H = 15, 8
        WH = (W, H)
        Between = 8
        OffsetY = 5

    class Default:
        Health = 3
        PauseTick = 1

    total_width = Heart.W * Default.Health + Heart.Between * (Default.Health - 1)

    def __init__(self, pos, size, color, stopwatch):
        super().__init__((0, 0), size, color)

        self.speed = Vec2(PlayerSettings.SpeedX, 1)
        self.movement = Vec2(PlayerSettings.MovementX, PlayerSettings.MovementY)

        self.Gravity = 100

        self.hitbox.center = pos

        self.health = Paddle.Default.Health
        # self.health = 1

        self.minimalHealth = -1
        self.bounces = 2

        self.target_y = self.hitbox.centery

        self.DoubleHeight = self.hitbox.h * 2
        self.H2draw = WindowConfigs.H + self.DoubleHeight

        self.__score = 0
        self.Stopwatch = stopwatch

        self.PauseBoards = [
            App.FontS.get_with_bg_texture("paused", "prstart", 12,
                                          Colors.BLACK.rgb, Colors.WHITE.rgb, 20, 3),

            App.FontS.get_with_bg_texture("paused", "prstart", 12,
                                          Colors.WHITE.rgb, Colors.BLACK.rgb, 20, 2)
        ]
        self.PauseTick = Paddle.Default.PauseTick
        self.isBlack = True
        self.Damaged = False
        self.SecondsDamaged = 0

        self.started = False
        self.StartText = Text(self.render, (0, 0), "[SPACE]", ("prstart", 12), Colors.WHITE)

        self.smoothness = 15.0

    def expand(self, value: int | float) -> None:
        '''
        Expands the paddle on x-axis with given value
        :param value:
        :return: None
        '''

        self.hitbox.w += value
        self.hitbox.x -= value / 2

    def damaged(self, seconds):
        self.Damaged = True
        self.SecondsDamaged = seconds

    def mouse_controls(self):
        target_x = Mouse.pos().x

        # Плавно двигаем центр ракетки к мышке
        self.hitbox.centerx = lerp(self.hitbox.centerx, target_x, self.smoothness * App.dt)

        # Твои проверки границ WindowConfigs...
        if self.hitbox.left < WindowConfigs.with_player_collision[0]:
            self.hitbox.left = WindowConfigs.with_player_collision[0]
        elif self.hitbox.right > WindowConfigs.with_player_collision[1]:
            self.hitbox.right = WindowConfigs.with_player_collision[1]

    def controls(self):

        keys = App.keys()

        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.hitbox.x += self.movement.x * self.speed.x * App.dt

        elif keys[pg.K_LEFT] or keys[pg.K_a]:
            self.hitbox.x -= self.movement.x * self.speed.x * App.dt

        # without player collision
        # if self.hitbox.left < WindowConfigs.Left:
        #     self.hitbox.left = WindowConfigs.Left
        # elif self.hitbox.right > WindowConfigs.right:
        #     self.hitbox.right = WindowConfigs.right

        # with player collision, 0 => left, 1 => right
        # WindowConfigs.Left + offsetX, WindowConfigs.right - offsetX
        if self.hitbox.left < WindowConfigs.with_player_collision[0]:
            self.hitbox.left = WindowConfigs.with_player_collision[0]
        elif self.hitbox.right > WindowConfigs.with_player_collision[1]:
            self.hitbox.right = WindowConfigs.with_player_collision[1]

    def death(self):
        self.hitbox.y += self.movement.y * self.speed.y * App.dt
        self.speed.y += self.Gravity * App.dt

        if self.bounces and self.hitbox.bottom > WindowConfigs.bottom:
            self.speed.y *= -1
            self.bounces -= 1

    def update(self):

        # off update
        if self.is_overdrawn:
            return

        if self.is_alive:
            self.hitbox.centery = lerp(self.hitbox.centery, self.target_y, self.smoothness * App.dt)

        # if self.is_dead and self.is_drawn:
        #     self.death()

        if self.is_dead:
            self.death()

        if self.Damaged:
            self.SecondsDamaged -= App.dt
            if self.SecondsDamaged < 0:
                self.Damaged = False

        if App.CurrentController == App.ControlMode.Keyboard:
            self.controls()
        elif App.CurrentController == App.ControlMode.Mouse:
            self.mouse_controls()

    @property
    def is_overdrawn(self):
        return self.pos.y > self.H2draw

    @property
    def is_drawn(self):
        return self.pos.y < self.H2draw

    @property
    def info(self):
        # return f"{self.time} {' ' * (3 - len(str(self.__score)))}score:{self.__score}"
        return f"{self.time}  {self.score}"

    @property
    def time(self):
        return self.Stopwatch.get_format("%h%.%m%.%s%")

    @property
    def score(self):
        return f"score:{self.__score}"

    def add_score(self, value):
        self.__score += value

    def bounce(self, y: int | float):
        self.target_y += y

    def draw(self):

        # off draw
        if self.is_overdrawn:
            return

        if self.Damaged or self.is_dead:
            draw_circular(
                self.render, self.hitbox,
                color=self.color.rgb, dash_len=15, gap_len=10, width=3, speed=60
            )
        else:
            super().draw()

        for i in range(min(self.health, self.Default.Health)):
            pos = (
                self.hitbox.right - Paddle.Heart.W - i * (Paddle.Heart.W + Paddle.Heart.Between),
                self.hitbox.bottom + Paddle.Heart.OffsetY
            )
            self.render.draw_color = Colors.BLACK.rgb
            self.render.fill_rect(pg.Rect(pos, Paddle.Heart.WH))

        if self.started:
            App.FontS.draw_text(
                text=self.time,
                name="prstart",
                size=12,
                color=Colors.BLACK.rgb,
                pos=(self.hitbox.left + 10, self.hitbox.top - 18)
            )

            App.FontS.draw_text(
                text=self.score,
                name="prstart",
                size=12,
                color=Colors.BLACK.rgb,
                pos=(self.hitbox.right - len(self.score) * 12, self.hitbox.top - 18)
            )

            if App.Runtime.IsPause:

                if self.PauseTick < 0:
                    self.PauseTick = Paddle.Default.PauseTick
                    self.isBlack = not self.isBlack

                self.PauseTick -= App.dt

                board = self.PauseBoards[self.isBlack]
                rect = board.get_rect()

                board.draw(dstrect=(self.hitbox.left, self.hitbox.top - rect.h - 2, rect.w, rect.h))

        else:
            self.StartText.rect.center = self.hitbox.center
            self.StartText.draw()
