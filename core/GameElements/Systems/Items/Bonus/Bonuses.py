from Event.CommandStuff.Command import Command
from Libraries.Python.Mixin import InspectorMixin
from Libraries.SimplePyGame.Colors import Colors
from Libraries.SimplePyGame.Positions import Vec2
from core.GameElements.Systems.Items.Bonus.Bonus import Bonus
from core.GameElements.Systems.Items.Bonus.BonusColors import BonusColors


class Bonuses:
    class Default:
        SIZE = Vec2.One * 35

        class Color(InspectorMixin):
            WIDE_PADDLE = BonusColors(Colors.GREEN, Colors.WHITE, Colors.BLACK)
            SPEED_BALL = BonusColors(Colors.YELLOW, Colors.WHITE, Colors.BLACK)
            ADDED_BALL = BonusColors(Colors.BLUE, Colors.WHITE, Colors.BLACK)
            ADDED_STICKY_BALL = BonusColors(Colors.CYAN, Colors.WHITE, Colors.BLACK)
            GUN_PISTOLS = BonusColors(Colors.RED, Colors.WHITE, Colors.BLACK)
            GIVE_LIFE = BonusColors(Colors.PINK, Colors.WHITE, Colors.BLACK)

    @staticmethod
    def bonus(pos: Vec2, _type: int, command: Command = None):
        return Bonus(size=Bonuses.Default.SIZE, color=Bonuses.Default.Color.get_all_values()[_type], pos=pos,
                     command=command, _type=_type)

    @staticmethod
    def wide_paddle(pos: Vec2, _type: int, command: Command = None) -> Bonus:
        return Bonus(size=Bonuses.Default.SIZE, color=Bonuses.Default.Color.WIDE_PADDLE, pos=pos, command=command,
                     _type=_type)

    @staticmethod
    def speed_ball(pos: Vec2, _type: int, command: Command = None) -> Bonus:
        return Bonus(size=Bonuses.Default.SIZE, color=Bonuses.Default.Color.SPEED_BALL, pos=pos, command=command,
                     _type=_type)

    @staticmethod
    def add_ball(pos: Vec2, _type: int, command: Command = None) -> Bonus:
        return Bonus(size=Bonuses.Default.SIZE, color=Bonuses.Default.Color.ADDED_BALL, pos=pos, command=command,
                     _type=_type)

    @staticmethod
    def add_sticky_ball(pos: Vec2, _type: int, command: Command = None) -> Bonus:
        return Bonus(size=Bonuses.Default.SIZE, color=Bonuses.Default.Color.ADDED_STICKY_BALL, pos=pos, command=command,
                     _type=_type)

    @staticmethod
    def activate_pistols(pos: Vec2, _type: int, command: Command = None) -> Bonus:
        return Bonus(size=Bonuses.Default.SIZE, color=Bonuses.Default.Color.GUN_PISTOLS, pos=pos, command=command,
                     _type=_type)


def main():
    pass


if __name__ == "__main__":
    main()
