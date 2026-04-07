from unittest.mock import DEFAULT

from Libraries.Python.Command import Command
from Libraries.SimplePyGame.Colors import Colors
from Libraries.SimplePyGame.Positions import Vec2
from core.GameElements.Systems.Items.Bonus.Bonus import Bonus
from core.GameElements.Systems.Items.Bonus.BonusColors import BonusColors


class Bonuses:
    class Default:
        SIZE = Vec2.One * 35
        COLOR_WIDE_PADDLE = BonusColors(Colors.GREEN, Colors.WHITE, Colors.BLACK)
        COLOR_SPEED_BALL = BonusColors(Colors.YELLOW, Colors.WHITE, Colors.BLACK)

    # Wide_Paddle = Bonus(DEFAULT_SIZE, )
    # Speed_Ball = Bonus(DEFAULT_SIZE)

    @staticmethod
    def wide_paddle(pos: Vec2, command: Command = None) -> Bonus:
        return Bonus(size=Bonuses.Default.SIZE, color=Bonuses.Default.COLOR_WIDE_PADDLE, pos=pos, command=command)

    @staticmethod
    def speed_ball(pos: Vec2, command: Command = None) -> Bonus:
        return Bonus(size=Bonuses.Default.SIZE, color=Bonuses.Default.COLOR_SPEED_BALL, pos=pos, command=command)


def main():
    pass


if __name__ == "__main__":
    main()
