from Libraries.SimplePyGame.SDL2.UI.Rectangle import Rectangle


class Bonus(Rectangle):

    def __init__(self, pos, size, color, render=None):

        super().__init__(pos, size, color, render)



    def draw(self):
        # super().draw()


        self.render.draw_color = self.color.rgba
        self.render.fill_rect(self.hitbox)