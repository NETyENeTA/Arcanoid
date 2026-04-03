import pygame
from pygame._sdl2 import Texture
import math
import random


class CelestialBody:
    def __init__(self, name, pts_count, r, orb, speed, col, rend, font):
        self.name, self.r, self.orb, self.speed, self.color = name, r, orb, speed, col
        self.angle = random.random() * 6.28
        self.hud_alpha = 0.0
        self.moons = []
        self.pos = [0, 0, 0]

        # Точки сферы
        self.pts = []
        phi = math.pi * (3. - math.sqrt(5.))
        for i in range(pts_count):
            y = 1 - (i / (pts_count - 1)) * 2
            rad = math.sqrt(1 - y * y)
            theta = phi * i
            self.pts.append([math.cos(theta) * rad * r, y * r, math.sin(theta) * rad * r, col])

        # Орбита
        self.orbit_path = []
        if orb > 0:
            samples = 128
            for i in range(samples + 1):
                ang = (i / samples) * math.pi * 2
                self.orbit_path.append([math.cos(ang) * orb, 0, math.sin(ang) * orb])

        # Текстуры HUD
        surf = font.render(name, True, col)
        self.t_tex = Texture.from_surface(rend, surf)
        self.t_size = surf.get_size()

    def update(self, dt, center_pos=[0, 0, 0]):
        self.angle += self.speed * dt * 10
        self.pos = [
            center_pos[0] + math.cos(self.angle) * self.orb,
            center_pos[1],
            center_pos[2] + math.sin(self.angle) * self.orb
        ]
        for m in self.moons:
            m.update(dt, self.pos)
