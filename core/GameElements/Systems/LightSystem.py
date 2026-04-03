from Libraries.SimplePyGame.Color import Color
from Libraries.SimplePyGame.Positions import Vec2
from core.GameElements.SystemItems.Light import Light


class LightSystem:


    def __init__(self):

        self.Lights = []


    def add_light(self, light: Light):
        self.Lights.append(light)

    def add(self, pos: Vec2, color: Color, render):
        self.Lights.append(Light(pos, color, render))


    def draw_debug(self):
        for light in self.Lights:
            light.draw()
