from collections.abc import Callable

from pygame._sdl2.video import Renderer

from Event.CommandStuff.Command import Command
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
        GUN_PISTOLS = 4
        GIVE_LIFE = 5

    def __init__(self, paddle: Paddle, add_ball: Callable, add_sticky_ball: Callable, rise_speed_ball: Callable,
                 activate_gun: Callable,
                 render: Renderer = None):

        self.render = render if render else App.Screen.render

        self.Bonuses: list[Bonus] = []

        self.paddle = paddle

        self.Command_Wide_Paddle = Command(self.paddle.expand, 10)
        self.Command_Speed_Ball = Command(rise_speed_ball)
        self.Command_Add_Ball = Command(add_ball, radius=14)
        self.Command_Sticky_Ball = Command(add_sticky_ball, radius=14)
        self.Command_Activate_Pistols = Command(activate_gun)
        self.Command_Give_Life = Command(self.__add_health_paddle)
        self.is_stickyBall_here = False

    def __add_health_paddle(self):
        if self.paddle.hp >= self.paddle.Default.Health:
            self.paddle.add_score(30)
            return
        self.paddle.hp += 1

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

            # 1. Нельзя второй Sticky, если он уже есть
            is_sticky_limit = self.is_stickyBall_here and type_bonus == BonusSystem.Types.ADD_STICKY_BALL
            # 2. Нельзя бонус Жизни, если HP полное
            is_hp_full = type_bonus == BonusSystem.Types.GIVE_LIFE and self.paddle.hp >= self.paddle.Default.Health

            if not is_sticky_limit and not is_hp_full:
                self.add(pos, type_bonus)

    def add(self, pos: Vec2, _type: Types | int):

        bonus: Bonus

        # _type = BonusSystem.Types.SPEED_BALL

        match _type:
            case BonusSystem.Types.WIDE_PADDLE:
                bonus = Bonuses.bonus(pos, _type, self.Command_Wide_Paddle)

            case BonusSystem.Types.SPEED_BALL:
                bonus = Bonuses.bonus(pos, _type, self.Command_Speed_Ball)

            case BonusSystem.Types.ADD_BALL:
                bonus = Bonuses.bonus(pos, _type, self.Command_Add_Ball)

            case BonusSystem.Types.ADD_STICKY_BALL:
                self.is_stickyBall_here = True
                bonus = Bonuses.bonus(pos, _type, self.Command_Sticky_Ball)

            case BonusSystem.Types.GUN_PISTOLS:
                bonus = Bonuses.bonus(pos, _type, self.Command_Activate_Pistols)

            case BonusSystem.Types.GIVE_LIFE:
                bonus = Bonuses.bonus(pos, _type, self.Command_Give_Life)

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
