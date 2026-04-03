import pygame
from pygame._sdl2 import Window, Renderer, Texture
import math
import random

# --- КОНСТАНТЫ ---
WIDTH, HEIGHT = 1600, 900
pygame.init()
FONT = pygame.font.SysFont("Arial", 22, bold=True)


class CelestialBody:
    def __init__(self, name, pts_count, r, orb, speed, col, rend):
        self.name, self.r, self.orb, self.speed, self.color = name, r, orb, speed, col
        self.angle = random.random() * 6.28
        self.hud_alpha = 0.0
        self.moons = []
        self.has_rings = False
        self.pos = [0, 0, 0]

        # Генерация точек сферы
        self.pts = []
        phi = math.pi * (3. - math.sqrt(5.))
        for i in range(pts_count):
            y = 1 - (i / (pts_count - 1)) * 2
            rad = math.sqrt(1 - y * y)
            theta = phi * i
            self.pts.append([math.cos(theta) * rad * r, y * r, math.sin(theta) * rad * r, col])

        # Текстура HUD
        surf = FONT.render(name, True, col)
        self.t_tex = Texture.from_surface(rend, surf)
        self.t_size = surf.get_size()

    def update(self, dt, center_pos=(0, 0, 0)):
        self.angle += self.speed * dt * 15
        self.pos = [
            center_pos[0] + math.cos(self.angle) * self.orb,
            center_pos[1],
            center_pos[2] + math.sin(self.angle) * self.orb
        ]
        for m in self.moons: m.update(dt, self.pos)


class SpaceEngine:
    def __init__(self):
        self.win = Window("Solar Explorer - Target System", size=(WIDTH, HEIGHT))
        self.rend = Renderer(self.win)
        self.rend.logical_size = (WIDTH, HEIGHT)

        self.cam = [0, 1500, -5000]
        self.vel = [0.0, 0.0, 0.0]
        self.yaw = self.pitch = 0.0

        self.planets = self.init_system()
        self.target = self.planets[0]  # По умолчанию смотрим на Солнце

        self.stars = [[random.randint(-15000, 15000) for _ in range(3)] for _ in range(2500)]
        self.asteroids = [{"d": random.uniform(1050, 1200), "a": random.random() * 6, "y": random.uniform(-20, 20),
                           "s": random.uniform(0.1, 0.2)} for _ in range(1000)]
        self.solar_time = 0

    def init_system(self):
        data = [
            ("SUN", 1000, 95, 0, 0, (255, 200, 20)),
            ("MERCURY", 80, 8, 300, 0.04, (170, 170, 170)),
            ("VENUS", 120, 16, 500, 0.03, (240, 230, 180)),
            ("EARTH", 150, 18, 750, 0.02, (60, 160, 255)),
            ("MARS", 120, 12, 1000, 0.015, (255, 80, 50)),
            ("JUPITER", 400, 55, 1400, 0.008, (220, 180, 140)),
            ("SATURN", 350, 45, 1850, 0.006, (210, 200, 150)),
            ("URANUS", 250, 30, 2250, 0.004, (160, 240, 240)),
            ("NEPTUNE", 250, 29, 2650, 0.003, (80, 100, 255)),
        ]
        planets = []
        for n, p, r, orb, s, c in data:
            obj = CelestialBody(n, p, r, orb, s, c, self.rend)
            if n == "EARTH": obj.moons.append(CelestialBody("MOON", 40, 5, 55, 0.1, (200, 200, 200), self.rend))
            if n == "JUPITER":
                obj.moons.append(CelestialBody("IO", 35, 4, 90, 0.08, (255, 255, 100), self.rend))
                obj.moons.append(CelestialBody("EUROPA", 35, 4, 120, 0.06, (200, 230, 255), self.rend))
            if n == "SATURN":
                obj.has_rings = True
                obj.ring_pts = [[math.cos(a) * r, random.uniform(-1, 1), math.sin(a) * r, (180, 170, 150)]
                                for r, a in [(random.uniform(75, 135), random.uniform(0, 6.28)) for _ in range(400)]]
            planets.append(obj)
        return planets

    def handle_input(self, dt):
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return False
            if e.type == pygame.KEYDOWN:
                if pygame.K_1 <= e.key <= pygame.K_9:
                    idx = e.key - pygame.K_1
                    if idx < len(self.planets): self.target = self.planets[idx]

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]: return False

        # --- LOOK AT TARGET ---
        dx, dy, dz = self.target.pos[0] - self.cam[0], self.target.pos[1] - self.cam[1], self.target.pos[2] - self.cam[
            2]
        self.yaw, self.pitch = math.atan2(dx, dz), math.atan2(dy, math.sqrt(dx * dx + dz * dz))

        acc = 130.0 * (25.0 if keys[pygame.K_LSHIFT] else 1.0)
        sy, cy, sp, cp = math.sin(self.yaw), math.cos(self.yaw), math.sin(self.pitch), math.cos(self.pitch)

        if keys[pygame.K_w]: self.vel[0] += sy * cp * acc; self.vel[1] -= sp * acc; self.vel[2] += cy * cp * acc
        if keys[pygame.K_s]: self.vel[0] -= sy * cp * acc; self.vel[1] += sp * acc; self.vel[2] -= cy * cp * acc
        if keys[pygame.K_a]: self.vel[0] -= cy * acc; self.vel[2] += sy * acc
        if keys[pygame.K_d]: self.vel[0] += cy * acc; self.vel[2] -= sy * acc
        if keys[pygame.K_LCTRL]: self.vel[1] += acc
        if keys[pygame.K_SPACE]: self.vel[1] -= acc
        return True

    def project(self, tx, ty, tz, fov, shake, sy, cy, sp, cp):
        rx, rz = tx * cy - tz * sy, tx * sy + tz * cy
        ry, rz = ty * cp - rz * sp, ty * sp + rz * cp
        if rz <= 10: return None
        f = fov / rz
        return (rx * f + WIDTH // 2 + shake, ry * f + HEIGHT // 2 + shake, rz, f)

    def render(self):
        self.rend.draw_color = (2, 2, 12, 255);
        self.rend.clear()
        speed = math.sqrt(sum(v * v for v in self.vel))
        shake, fov = (random.uniform(-1, 1) * speed * 0.005), 950 + speed * 0.06
        sy, cy, sp, cp = math.sin(self.yaw), math.cos(self.yaw), math.sin(self.pitch), math.cos(self.pitch)

        # 1. Stars
        for s in self.stars:
            p1 = self.project(s[0] - self.cam[0], s[1] - self.cam[1], s[2] - self.cam[2], fov, shake, sy, cy, sp, cp)
            if p1:
                t = 0.0001 + speed * 0.00012
                p2 = self.project(s[0] - self.cam[0] - self.vel[0] * t, s[1] - self.cam[1] - self.vel[1] * t,
                                  s[2] - self.cam[2] - self.vel[2] * t, fov, shake, sy, cy, sp, cp)
                self.rend.draw_color = (int(min(255, 160 + speed * 0.05)), 180, 255, 255)
                if p2: self.rend.draw_line((p1[0], p1[1]), (p2[0], p2[1]))

        # 2. Collect & Sort
        rq, hud = [], []
        for ast in self.asteroids:
            ax, az = math.cos(ast["a"]) * ast["d"], math.sin(ast["a"]) * ast["d"]
            pr = self.project(ax - self.cam[0], ast["y"] - self.cam[1], az - self.cam[2], fov, shake, sy, cy, sp, cp)
            if pr: rq.append((*pr, (110, 105, 100), 0.8))

        for p in self.planets:
            if p.name == "SUN":
                for _ in range(6):
                    t, ang = self.solar_time * 3 + _, _ * 0.8
                    pr = self.project(math.cos(ang) * (95 + math.sin(t) * 12) - self.cam[0],
                                      math.cos(t * 2) * 15 - self.cam[1],
                                      math.sin(ang) * (95 + math.sin(t) * 12) - self.cam[2], fov, shake, sy, cy, sp, cp)
                    if pr: rq.append((*pr, (255, 130, 0), 4))

            for obj in [p] + p.moons:
                dist = math.sqrt(sum((obj.pos[i] - self.cam[i]) ** 2 for i in range(3)))
                obj.hud_alpha += ((1.0 if dist < (3000 if obj == p else 800) else 0.0) - obj.hud_alpha) * 0.1
                pr = self.project(obj.pos[0] - self.cam[0], obj.pos[1] - self.cam[1], obj.pos[2] - self.cam[2], fov,
                                  shake, sy, cy, sp, cp)
                if pr:
                    if obj.hud_alpha > 0.01: hud.append((obj, pr))
                    for pt in obj.pts:
                        pr_pt = self.project(pt[0] + obj.pos[0] - self.cam[0], pt[1] + obj.pos[1] - self.cam[1],
                                             pt[2] + obj.pos[2] - self.cam[2], fov, shake, sy, cy, sp, cp)
                        if pr_pt: rq.append((*pr_pt, pt[3], 2 if obj == p else 1.5))

            if p.has_rings:
                for rpt in p.ring_pts:
                    pr = self.project(rpt[0] + p.pos[0] - self.cam[0], rpt[1] + p.pos[1] - self.cam[1],
                                      rpt[2] + p.pos[2] - self.cam[2], fov, shake, sy, cy, sp, cp)
                    if pr: rq.append((*pr, rpt[3], 1))

        rq.sort(key=lambda x: x[2], reverse=True)
        for x, y, z, f, col, sz in rq:
            sh = max(0.1, min(1.0, 5000 / (z + 2500)))
            self.rend.draw_color = (int(col[0] * sh), int(col[1] * sh), int(col[2] * sh), 255)
            self.rend.fill_rect((int(x), int(y), max(1, int(sz * f * 1.5)), max(1, int(sz * f * 1.5))))

        for obj, pr in hud:
            obj.t_tex.alpha = int(obj.hud_alpha * 255)
            self.rend.draw_color = (*obj.color, int(obj.hud_alpha * 180))
            oy = 75 + (1.0 - obj.hud_alpha) * 30
            self.rend.draw_line((pr[0], pr[1]), (pr[0], pr[1] - int(oy) + 12))
            r, L = int(obj.r * (fov / pr[2])) + 12, 15
            for s1, s2 in [(-1, -1), (1, 1), (-1, 1), (1, -1)]:
                self.rend.draw_line((pr[0] + s1 * r, pr[1] + s2 * r), (pr[0] + s1 * r - s1 * L, pr[1] + s2 * r))
                self.rend.draw_line((pr[0] + s1 * r, pr[1] + s2 * r), (pr[0] + s1 * r, pr[1] + s2 * r - s2 * L))
            self.rend.blit(obj.t_tex, pygame.Rect(int(pr[0] - obj.t_size[0] // 2), int(pr[1] - int(oy)), obj.t_size[0],
                                                  obj.t_size[1]))
        self.rend.present()

    def run(self):
        c = pygame.time.Clock()
        while True:
            dt = c.tick(60) / 1000.0
            self.solar_time += dt
            if not self.handle_input(dt): break
            self.cam[0] += self.vel[0] * dt;
            self.cam[1] += self.vel[1] * dt;
            self.cam[2] += self.vel[2] * dt
            for v in range(3): self.vel[v] *= 0.96
            for p in self.planets: p.update(dt)
            for a in self.asteroids: a["a"] += a["s"] * dt
            self.render()
        pygame.quit()


if __name__ == "__main__": SpaceEngine().run()
