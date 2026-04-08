from Libraries.SimplePyGame.Color import Color


class Colors:
    WHITE = Color.mono_color_alpha(255)
    BLACK = Color.mono_color_with_alpha(0, 255)
    GRAY = Color.mono_color_with_alpha(125, 255)

    RED = Color(255, 0, 0)
    GREEN = Color(0, 255, 0)
    BLUE = Color(0, 0, 255)

    PINK = Color(255, 0, 160)

    YELLOW = Color(255, 255, 0)

    WHITE_Alpha_0 = Color.mono_color_with_alpha(255, 0)
    Black_Alpha_0 = Color.mono_color_alpha(0)

    GOLD = Color(255,125, 0)
    CYAN = Color(0, 255, 255)
