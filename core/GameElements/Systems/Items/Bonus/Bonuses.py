from Event.CommandStuff.Command import Command
from Libraries.Python.Mixin import InspectorMixin
from Libraries.SimplePyGame.Colors import Colors, Color
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
            STICKY_PADDLE = BonusColors(Color(150,255,150), Colors.WHITE, Colors.BLACK)
            MIRROR_PADDLE = BonusColors(Color(150,150,255), Colors.WHITE, Colors.BLACK)


        class FakeRates(InspectorMixin):
            WIDE_PADDLE = 0.4
            SPEED_BALL = 0.6
            ADDED_BALL = 0.7
            ADDED_STICKY_BALL = 0.5
            GUN_PISTOLS = 0.4
            GIVE_LIFE = 0.8
            STICKY_PADDLE = 0.2
            MIRROR_PADDLE = 0.2


    @staticmethod
    def bonus(pos: Vec2, _type: int, command: Command = None):
        return Bonus(size=Bonuses.Default.SIZE, color=Bonuses.Default.Color.get_all_values()[_type], pos=pos,
                     command=command, _type=_type, fake_rate=Bonuses.Default.FakeRates.get_all_values()[_type])


def main():
    pass


if __name__ == "__main__":
    main()
