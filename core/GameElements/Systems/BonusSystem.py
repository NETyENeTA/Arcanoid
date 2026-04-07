from collections.abc import Callable

from pygame._sdl2.video import Renderer

from Libraries.Python.Command import Command
from Libraries.Python.Mixin import InspectorMixin
from Libraries.SimplePyGame.Positions import Vec2
from core.App import AppConfigs as App, WindowConfig as WC
from core.GameElements.Paddle import Paddle
from core.GameElements.Systems.Items.Bonus.Bonus import Bonus
from core.GameElements.Systems.Items.Bonus.Bonuses import Bonuses

from random import random, choice


class BonusSystem:
    class Types(InspectorMixin):
        WIDE_PADDLE = 0
        SPEED_BALL = 1
        ADD_BALL = 2
        ADD_STICKY_BALL = 3

    def __init__(self, paddle: Paddle, add_ball: Callable, add_sticky_ball: Callable,
                 render: Renderer = None):

        self.render = render if render else App.Screen.render

        self.Bonuses: list[Bonus] = []

        self.paddle = paddle

        self.Command_Wide_Paddle = Command(self.paddle.expand, 10)
        self.Command_Speed_Ball = Command(None)
        self.Command_Add_Ball = Command(add_ball, radius=14)
        self.Command_Sticky_Ball = Command(add_sticky_ball, radius=14)

        self.is_stickyBall_here = False

    def clear_status(self):
        self.is_stickyBall_here = False

    def add_bonus(self, bonus: Bonus):
        self.Bonuses.append(bonus)

    def is_check_bonus_in(self, _type) -> bool:

        for bonus in self.Bonuses:
            if bonus.type == _type:
                return True

        return False

    def spawn(self, pos: Vec2, rate: float | int = 0.2):

        if random() < rate:
            type_bonus = choice(BonusSystem.Types.get_all_values())
            if not self.is_stickyBall_here:
                self.add(pos, type_bonus)

    def add(self, pos: Vec2, _type: Types | int):

        bonus: Bonus

        # _type = BonusSystem.Types.ADD_STICKY_BALL

        match _type:
            case BonusSystem.Types.WIDE_PADDLE:
                bonus = Bonuses.wide_paddle(pos, _type, self.Command_Wide_Paddle)

            case BonusSystem.Types.SPEED_BALL:
                bonus = Bonuses.speed_ball(pos, _type, self.Command_Speed_Ball)

            case BonusSystem.Types.ADD_BALL:
                # self.Command_Add_Ball.kwargs['pos'] = pos
                bonus = Bonuses.add_ball(pos, _type, self.Command_Add_Ball)

            case BonusSystem.Types.ADD_STICKY_BALL:
                # self.Command_Add_Ball.kwargs['pos'] = pos
                self.is_stickyBall_here = True
                bonus = Bonuses.add_sticky_ball(pos, _type, self.Command_Sticky_Ball)

            case _:
                raise TypeError("Bonus type not supported")

        self.Bonuses.append(bonus)

    def is_collided_with_paddle(self, bonus: Bonus) -> bool:
        return self.paddle.hitbox.colliderect(bonus.hitbox)

    def update(self):

        for bonus in self.Bonuses:
            bonus.update()

            if bonus.hitbox.top > WC.H:
                if self.is_check_bonus_in(BonusSystem.Types.ADD_STICKY_BALL):
                    self.is_stickyBall_here = False
                self.Bonuses.remove(bonus)

            if self.is_collided_with_paddle(bonus):
                bonus.Command()
                self.Bonuses.remove(bonus)

    def cast_shadows(self):
        for bonus in self.Bonuses:
            bonus.cast_shadow()

    def draw(self):
        for bonus in self.Bonuses:
            bonus.draw()


def main():
    pass


if __name__ == "__main__":
    main()
