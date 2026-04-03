import pygame, math, random
from pygame._sdl2 import Window, Renderer, Texture
from celestial import CelestialBody
from renderer import SpaceRenderer
from input_handler import InputHandler
from data import PLANETS_DATA, MOONS_DATA

WIDTH, HEIGHT = 1600, 900
pygame.init()
FONT = pygame.font.SysFont("Arial", 18, bold=True)
FPS = 165

class SpaceEngine:
    def __init__(self):
        self.win = Window("Solar Engine", size=(WIDTH, HEIGHT))
        self.rend = Renderer(self.win)
        self.gfx = SpaceRenderer(self.rend, WIDTH, HEIGHT)
        self.inputs = InputHandler()
        self.cam, self.vel = [0, 0, 0], [0.0, 0.0, 0.0]
        self.yaw, self.pitch = 0.0, 0.0
        self.cur_yaw, self.cur_pitch = 0.0, 0.0
        self.planets = self.init_system()
        self.target = self.planets[0]
        self.stars = [[random.randint(-15000, 15000) for _ in range(3)] for _ in range(2500)]
        self.solar_time = 0

        # СОЗДАЕМ ТЕКСТУРУ МЯГКОГО КРУГА
        glow_surf = pygame.Surface((128, 128), pygame.SRCALPHA)
        for r in range(64, 0, -1):
            alpha = int(255 * (r / 64) ** 2 * 0.15) # Плавное затухание
            pygame.draw.circle(glow_surf, (255, 180, 50, alpha), (64, 64), r)
        self.glow_tex = Texture.from_surface(self.rend, glow_surf)
        # Включаем режим смешивания для мягкости
        self.glow_tex.blend_mode = 1 # BLENDMODE_BLEND

    def init_system(self):
        planets = []
        for n, p, r, orb, s, c in PLANETS_DATA:
            planets.append(CelestialBody(n, p, r, orb, s, c, self.rend, FONT))
        for p_name, n, p, r, orb, s, c in MOONS_DATA:
            for pl in planets:
                if pl.name == p_name: pl.moons.append(CelestialBody(n, p, r, orb, s, c, self.rend, FONT))
        return planets

    def run(self):
        clock = pygame.time.Clock()
        while True:
            dt = min(clock.tick(FPS) / 1000.0, 0.1)
            self.solar_time += dt
            if not self.inputs.handle(self): break
            dx, dy, dz = self.target.pos[0]-self.cam[0], self.target.pos[1]-self.cam[1], self.target.pos[2]-self.cam[2]
            ty, tp = math.atan2(dx, dz), math.atan2(dy, math.sqrt(dx*dx + dz*dz))
            self.cur_yaw += ((ty - self.cur_yaw + math.pi) % (math.pi * 2) - math.pi) * 0.08
            self.cur_pitch += (tp - self.cur_pitch) * 0.08
            self.yaw, self.pitch = self.cur_yaw, self.cur_pitch
            for i in range(3): self.cam[i]+=self.vel[i]; self.vel[i]*=0.96
            for p in self.planets: p.update(dt)
            self.render()
        pygame.quit()

    def render(self):
        self.rend.draw_color = (2, 2, 15, 255);
        self.rend.clear()
        spd = math.sqrt(sum(v * v for v in self.vel))
        shk, fov = (random.uniform(-1, 1) * spd * 0.04), 950 + spd * 1.5
        sy, cy, sp, cp = math.sin(self.yaw), math.cos(self.yaw), math.sin(self.pitch), math.cos(self.pitch)

        # --- ОБЪЯВЛЯЕМ sun_pulse ТУТ ---
        sun_pulse = math.sin(self.solar_time * 3) * 8 + 15

        self.gfx.draw_stars(self.stars, self.cam, self.vel, sy, cy, sp, cp, fov, shk, spd)
        rq, hud = [], []
        for p in self.planets:
            # СВЕЧЕНИЕ СОЛНЦА
            if p.name == "SUN":
                pr_sun = self.gfx.project(p.pos, self.cam, sy, cy, sp, cp, fov, shk)
                if pr_sun:
                    sun_pulse = math.sin(self.solar_time * 3) * 15 + 20
                    for i in range(3):
                        # Увеличиваем размер для каждого слоя
                        glow_size = int((p.r * (fov / pr_sun[2])) * (2.0 + i * 0.8) + sun_pulse)
                        self.glow_tex.alpha = 150 // (i + 1)
                        rect = pygame.Rect(int(pr_sun[0]-glow_size//2), int(pr_sun[1]-glow_size//2), glow_size, glow_size)
                        self.rend.blit(self.glow_tex, rect)


            # ОРБИТЫ
            if p.orb > 0:
                is_t = (p.name == self.target.name)
                self.rend.draw_color = (*[int(c * (0.6 if is_t else 0.2)) for c in p.color], 255 if is_t else 40)
                for i in range(len(p.orbit_path) - 1):
                    p1 = self.gfx.project(p.orbit_path[i], self.cam, sy, cy, sp, cp, fov, shk)
                    p2 = self.gfx.project(p.orbit_path[i + 1], self.cam, sy, cy, sp, cp, fov, shk)
                    if p1 and p2: self.rend.draw_line((p1[0], p1[1]), (p2[0], p2[1]))

            # ТОЧКИ ТЕЛ
            for obj in [p] + p.moons:
                dist = math.dist(obj.pos, self.cam);
                is_t = (obj.name == self.target.name)
                obj.hud_alpha += ((1.0 if (dist < 3000 or is_t) else 0.0) - obj.hud_alpha) * 0.1
                pr = self.gfx.project(obj.pos, self.cam, sy, cy, sp, cp, fov, shk)
                if pr:
                    if obj.hud_alpha > 0.01: hud.append((obj, pr, dist, is_t))
                    for pt in obj.pts:
                        # Тень
                        shadow = max(0.1, min(1.0, (pt[0] * -obj.pos[0] + pt[2] * -obj.pos[2]) / (
                                    obj.r * obj.r) + 1.2)) if obj.name != "SUN" else 1.0
                        pr_pt = self.gfx.project([pt[i] + obj.pos[i] for i in range(3)], self.cam, sy, cy, sp, cp, fov,
                                                 shk)
                        if pr_pt: rq.append((*pr_pt, pt[3], shadow))

        # Рендерим отсортированные точки (меши планет)
        rq.sort(key=lambda x: x[2], reverse=True)
        for x, y, z, f, col, shd in rq:
            sh = max(0.1, min(1.0, 6000 / (z + 3000))) * shd
            self.rend.draw_color = (int(col[0] * sh), int(col[1] * sh), int(col[2] * sh), 255)
            self.rend.fill_rect(pygame.Rect(int(x - f // 2), int(y - f // 2), max(1, int(f)), max(1, int(f))))

        # HUD (надписи и рамки)
        for obj, pr, d, is_t in hud:
            obj.t_tex.alpha = int(obj.hud_alpha * 255);
            self.rend.draw_color = (*obj.color, int(obj.hud_alpha * 200))
            oy = 70 + (1.0 - obj.hud_alpha) * 30
            self.rend.draw_line((pr[0], pr[1]), (pr[0], pr[1] - int(oy) + 10))
            r, L = int(obj.r * (fov / pr[2])) + 12, 15
            corn = [(-1, -1), (1, 1), (-1, 1), (1, -1)] if is_t else [(-1, -1), (1, 1)]
            for s1, s2 in corn:
                self.rend.draw_line((pr[0] + s1 * r, pr[1] + s2 * r), (pr[0] + s1 * r - s1 * L, pr[1] + s2 * r))
                self.rend.draw_line((pr[0] + s1 * r, pr[1] + s2 * r), (pr[0] + s1 * r, pr[1] + s2 * r - s2 * L))
            self.rend.blit(obj.t_tex, pygame.Rect(int(pr[0] - obj.t_size[0] // 2), int(pr[1] - int(oy)), obj.t_size[0],
                                                  obj.t_size[1]))

            # Дистанция
            ds = FONT.render(f"{int(d)} KM", True, (220, 220, 220))
            dtex = Texture.from_surface(self.rend, ds)
            dtex.alpha = int(obj.hud_alpha * 180)
            self.rend.blit(dtex,
                           pygame.Rect(int(pr[0] - ds.get_width() // 2), int(pr[1] - int(oy) + 22), ds.get_width(),
                                       ds.get_height()))

        self.gfx.draw_radar(self.planets, self.cam, self.target)
        self.rend.present()


if __name__ == "__main__": SpaceEngine().run()
