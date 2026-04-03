import pygame, math, random
from pygame._sdl2 import Texture


class CelestialBody:
    def __init__(self, name, pts_count, r, orb, speed, col, rend, font):
        self.name, self.r, self.orb, self.speed, self.color = name, r, orb, speed, col
        self.angle = random.random() * 6.28
        self.rotation_speed = 0.8  # Скорость вращения вокруг оси
        self.hud_alpha = 0.0
        self.moons = []
        self.pos = [0, 0, 0]

        # ГЕНЕРАЦИЯ СФЕРЫ (Точки планеты)
        self.pts = []
        phi = math.pi * (3. - math.sqrt(5.))
        for i in range(pts_count):
            y = 1 - (i / (pts_count - 1)) * 2
            rad = math.sqrt(1 - y * y)
            theta = phi * i
            self.pts.append([math.cos(theta) * rad * r, y * r, math.sin(theta) * rad * r, col])

        # ГЕНЕРАЦИЯ КОЛЕЦ (Только для Сатурна и Урана, например)
        if name in ["SATURN", "URANUS"]:
            ring_color = (int(col[0] * 0.8), int(col[1] * 0.8), int(col[2] * 0.8))
            for _ in range(pts_count // 2):
                dist = random.uniform(r * 1.5, r * 2.2)  # Радиус колец
                ang = random.uniform(0, math.pi * 2)
                # Кольца лежат в плоскости XZ, но можно чуть наклонить по Y
                self.pts.append([math.cos(ang) * dist, random.uniform(-1, 1), math.sin(ang) * dist, ring_color])

        # ПРЕДРАСЧЕТ ОРБИТЫ
        self.orbit_path = []
        if orb > 0:
            for i in range(129):
                ang = (i / 128) * math.pi * 2
                self.orbit_path.append([math.cos(ang) * orb, 0, math.sin(ang) * orb])

        surf = font.render(name, True, col)
        self.t_tex = Texture.from_surface(rend, surf)
        self.t_size = surf.get_size()

    def update(self, dt, center_pos=[0, 0, 0]):
        # Движение по орбите
        self.angle += self.speed * dt * 10
        self.pos = [
            center_pos[0] + math.cos(self.angle) * self.orb,
            center_pos[1],
            center_pos[2] + math.sin(self.angle) * self.orb
        ]

        # ВРАЩЕНИЕ ВОКРУГ ОСИ (всех точек pts)
        rot_angle = self.rotation_speed * dt
        sn, cs = math.sin(rot_angle), math.cos(rot_angle)
        for i in range(len(self.pts)):
            px, py, pz, pcol = self.pts[i]
            # Вращаем вокруг оси Y
            nx = px * cs + pz * sn
            nz = -px * sn + pz * cs
            self.pts[i] = [nx, py, nz, pcol]

        for m in self.moons:
            m.update(dt, self.pos)
