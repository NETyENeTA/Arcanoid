import pygame
from pygame._sdl2 import Window, Renderer, Texture
import math, random
from celestial import CelestialBody
from renderer import SpaceRenderer
from data import PLANETS_DATA, MOONS_DATA

WIDTH, HEIGHT = 1600, 900
pygame.init()
FONT = pygame.font.SysFont("Arial", 18, bold=True)


class SpaceEngine:
    def __init__(self):
        self.win = Window("Solar Engine - Ultimate 4-File", size=(WIDTH, HEIGHT))
        self.rend = Renderer(self.win)
        self.gfx = SpaceRenderer(self.rend, WIDTH, HEIGHT)

        self.cam, self.vel = [0, 1500, -5000], [0.0, 0.0, 0.0]
        self.yaw, self.pitch = 0.0, 0.0
        self.cur_yaw, self.cur_pitch = 0.0, 0.0
        self.autopilot = False

        self.planets = self.init_system()
        self.target = self.planets[0]
        self.stars = [[random.randint(-15000, 15000) for _ in range(3)] for _ in range(2500)]
        self.solar_time = 0

    def init_system(self):
        planets = []
        for n, p, r, orb, s, c in PLANETS_DATA:
            obj = CelestialBody(n, p, r, orb, s, c, self.rend, FONT)
            if n == "SATURN":
                obj.has_rings = True
                obj.ring_pts = [[math.cos(a) * r, random.uniform(-1, 1), math.sin(a) * r, (180, 170, 150)]
                                for r, a in [(random.uniform(75, 135), random.uniform(0, 6.28)) for _ in range(400)]]
            planets.append(obj)
        for p_name, n, p, r, orb, s, c in MOONS_DATA:
            for pl in planets:
                if pl.name == p_name: pl.moons.append(CelestialBody(n, p, r, orb, s, c, self.rend, FONT))
        return planets

    def run(self):
        clock = pygame.time.Clock()
        while True:
            dt = min(clock.tick(60) / 1000.0, 0.1)
            self.solar_time += dt
            if not self.handle_events(): break
            self.update_physics(dt)
            self.render_frame()
        pygame.quit()

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return False
            if e.type == pygame.KEYDOWN:
                if pygame.K_1 <= e.key <= pygame.K_9:
                    idx = e.key - pygame.K_1
                    if idx < len(self.planets): self.target = self.planets[idx]
                if e.key == pygame.K_f: self.autopilot = not self.autopilot
        return True

    def update_physics(self, dt):
        dx, dy, dz = [self.target.pos[i] - self.cam[i] for i in range(3)]
        dist = math.sqrt(dx * dx + dy * dy + dz * dz)

        # Lerp Look-at
        ty, tp = math.atan2(dx, dz), math.atan2(dy, math.sqrt(dx * dx + dz * dz))
        self.cur_yaw += ((ty - self.cur_yaw + math.pi) % (math.pi * 2) - math.pi) * 0.08
        self.cur_pitch += (tp - self.cur_pitch) * 0.08
        self.yaw, self.pitch = self.cur_yaw, self.cur_pitch

        # Movement
        keys = pygame.key.get_pressed()
        sy, cy, sp, cp = math.sin(self.yaw), math.cos(self.yaw), math.sin(self.pitch), math.cos(self.pitch)

        acc = 180.0 * (25.0 if keys[pygame.K_LSHIFT] else 1.0)

        if self.autopilot and dist > 350:
            a_spd = 2200.0
            self.vel[0] += sy * cp * a_spd * dt;
            self.vel[1] -= sp * a_spd * dt;
            self.vel[2] += cy * cp * a_spd * dt
        else:
            if keys[pygame.K_w]:
                self.vel[0] += sy * cp * acc * dt;
                self.vel[1] -= sp * acc * dt;
                self.vel[2] += cy * cp * acc * dt
            if keys[pygame.K_s]:
                self.vel[0] -= sy * cp * acc * dt;
                self.vel[1] += sp * acc * dt;
                self.vel[2] -= cy * cp * acc * dt
            if keys[pygame.K_a]:
                self.vel[0] -= cy * acc * dt;
                self.vel[2] += sy * acc * dt
            if keys[pygame.K_d]:
                self.vel[0] += cy * acc * dt;
                self.vel[2] -= sy * acc * dt
            if keys[pygame.K_LCTRL]: self.vel[1] += acc * dt
            if keys[pygame.K_SPACE]: self.vel[1] -= acc * dt

        for i in range(3): self.cam[i] += self.vel[i]; self.vel[i] *= 0.96
        for p in self.planets: p.update(dt)

    def render_frame(self):
        self.rend.draw_color = (2, 2, 15, 255)
        self.rend.clear()
        spd = math.sqrt(sum(v * v for v in self.vel))
        shk, fov = (random.uniform(-1, 1) * spd * 0.04), 950 + spd * 1.5
        sy, cy, sp, cp = math.sin(self.yaw), math.cos(self.yaw), math.sin(self.pitch), math.cos(self.pitch)

        # 1. Звезды (Warp эффект теперь внутри)
        self.gfx.draw_stars(self.stars, self.cam, self.vel, sy, cy, sp, cp, fov, shk, spd)

        rq, hud = [], []
        # --- ОТРИСОВКА ОРБИТ ---
        for p in self.planets:
            if p.orb > 0:
                # Сравниваем по имени, чтобы точно поймать цель
                is_target_orb = (p.name == self.target.name)

                if is_target_orb:
                    # Яркая и насыщенная орбита для цели
                    orb_alpha = 255
                    r_o, g_o, b_o = p.color
                    # Делаем цвет чуть светлее для цели
                    self.rend.draw_color = (min(255, r_o + 50), min(255, g_o + 50), min(255, b_o + 50), orb_alpha)
                else:
                    # Тусклая орбита для остальных
                    orb_alpha = 40
                    r_o, g_o, b_o = p.color
                    self.rend.draw_color = (int(r_o * 0.3), int(g_o * 0.3), int(b_o * 0.3), orb_alpha)

                for i in range(len(p.orbit_path) - 1):
                    p1 = self.gfx.project(p.orbit_path[i], self.cam, sy, cy, sp, cp, fov, shk)
                    p2 = self.gfx.project(p.orbit_path[i + 1], self.cam, sy, cy, sp, cp, fov, shk)

                    if p1 and p2:
                        self.rend.draw_line((p1[0], p1[1]), (p2[0], p2[1]))
                        # Если это цель, рисуем линию дважды со смещением для "толщины"
                        if is_target_orb:
                            self.rend.draw_line((p1[0] + 1, p1[1]), (p2[0] + 1, p2[1]))

            # Объекты (планеты + луны)
            for obj in [p] + p.moons:
                dist = math.dist(obj.pos, self.cam)
                is_t = (obj == self.target)
                obj.hud_alpha += ((1.0 if (dist < 3000 or is_t) else 0.0) - obj.hud_alpha) * 0.1
                pr = self.gfx.project(obj.pos, self.cam, sy, cy, sp, cp, fov, shk)
                if pr:
                    if obj.hud_alpha > 0.01: hud.append((obj, pr, dist, is_t))
                    for pt in obj.pts:
                        p_pos = [pt[i] + obj.pos[i] for i in range(3)]
                        pr_pt = self.gfx.project(p_pos, self.cam, sy, cy, sp, cp, fov, shk)
                        if pr_pt:
                            rq.append((*pr_pt, pt[3], 2 if obj == p else 1.2))

        # 3. Отрисовка тел
        rq.sort(key=lambda x: x[2], reverse=True)
        for x, y, z, f, col, sz in rq:
            sh = max(0.1, min(1.0, 6000 / (z + 3000)))
            self.rend.draw_color = (int(col[0] * sh), int(col[1] * sh), int(col[2] * sh), 255)
            rect_sz = max(1, int(sz * f))
            self.rend.fill_rect(pygame.Rect(int(x - rect_sz // 2), int(y - rect_sz // 2), rect_sz, rect_sz))

        # 4. HUD (Километраж и Рамки)
        for obj, pr, d, is_t in hud:
            obj.t_tex.alpha = int(obj.hud_alpha * 255)
            r_h, g_h, b_h = obj.color
            self.rend.draw_color = (r_h, g_h, b_h, int(obj.hud_alpha * 200))
            px, py = pr[0], pr[1]
            oy = 70 + (1.0 - obj.hud_alpha) * 30
            self.rend.draw_line((px, py), (px, py - int(oy) + 10))

            r_f, L = int(obj.r * (fov / pr[2])) + 12, 15
            corn = [(-1, -1), (1, 1), (-1, 1), (1, -1)] if is_t else [(-1, -1), (1, 1)]
            for s1, s2 in corn:
                self.rend.draw_line((px + s1 * r_f, py + s2 * r_f), (px + s1 * r_f - s1 * L, py + s2 * r_f))
                self.rend.draw_line((px + s1 * r_f, py + s2 * r_f), (px + s1 * r_f, py + s2 * r_f - s2 * L))

            self.rend.blit(obj.t_tex,
                           pygame.Rect(int(px - obj.t_size[0] / 2), int(py - int(oy)), obj.t_size[0], obj.t_size[1]))

            # --- ДИСТАНЦИЯ ---
            dist_surf = FONT.render(f"{int(d)} KM", True, (220, 220, 220))
            dist_tex = Texture.from_surface(self.rend, dist_surf)
            dist_tex.alpha = int(obj.hud_alpha * 180)
            self.rend.blit(dist_tex, pygame.Rect(int(px - dist_surf.get_width() / 2), int(py - int(oy) + 22),
                                                 dist_surf.get_width(), dist_surf.get_height()))

        self.gfx.draw_radar(self.planets, self.cam, self.target)
        self.rend.present()


if __name__ == "__main__":
    SpaceEngine().run()
