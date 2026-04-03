import pygame
from pygame._sdl2 import Window, Renderer
import math
import random

pygame.init()
W, H = 1600, 800
win = Window("Lizard: Flying Wings & Super Fly", size=(W, H))
rend = Renderer(win)


def lerp(a, b, f):
    if isinstance(a, (list, tuple)):
        return [a[i] + f * (b[i] - a[i]) for i in range(len(a))]
    return a + f * (b - a)


# --- ПАРАМЕТРЫ ТЕЛА ---
NUM_SEG = 28
SEG_DIST = 9
segments = [[W // 2, H // 2] for _ in range(NUM_SEG)]
wave_offset = 0.0
swallowed_foods = []


# --- МУХИ С КРЫЛЬЯМИ ---
class Fly:
    def __init__(self, is_super=False):
        self.pos = [random.randint(100, W - 100), random.randint(100, H - 100)]
        self.vel = [0.0, 0.0]
        self.angle = random.uniform(0, math.pi * 2)
        self.tired_timer = 0
        self.is_caught = False
        self.is_super = is_super
        self.wing_swing = 0.0

    def update(self, head_pos):
        if self.is_caught: return
        d = math.hypot(self.pos[0] - head_pos[0], self.pos[1] - head_pos[1])

        # Крылья машут, если муха не спит
        if self.tired_timer <= 0:
            self.wing_swing += 0.8 if not self.is_super else 1.2

        if d < 150:  # Испуг
            self.tired_timer = 0
            ang = math.atan2(self.pos[1] - head_pos[1], self.pos[0] - head_pos[0])
            self.vel[0] += math.cos(ang) * (2.0 if self.is_super else 1.5)
            self.vel[1] += math.sin(ang) * (2.0 if self.is_super else 1.5)
        elif self.tired_timer > 0:
            self.tired_timer -= 1
            self.vel = [v * 0.8 for v in self.vel]
        else:
            self.angle += random.uniform(-0.2, 0.2)
            speed = 0.7 if self.is_super else 0.4
            self.vel[0] += math.cos(self.angle) * speed
            self.vel[1] += math.sin(self.angle) * speed
            if random.random() < 0.01: self.tired_timer = random.randint(40, 100)

        self.pos[0] = (self.pos[0] + self.vel[0]) % W
        self.pos[1] = (self.pos[1] + self.vel[1]) % H
        self.vel = [v * (0.95 if self.is_super else 0.93) for v in self.vel]

    def draw(self, renderer):
        if self.is_caught: return
        x, y = int(self.pos[0]), int(self.pos[1])
        # Крылья (белые полупрозрачные)
        w_size = 5 if not self.is_super else 7
        w_offset = math.sin(self.wing_swing) * w_size
        renderer.draw_color = (200, 200, 255, 150)
        renderer.draw_line((x, y), (int(x - 6), int(y - w_offset)))
        renderer.draw_line((x, y), (int(x + 6), int(y - w_offset)))
        # Тельце
        renderer.draw_color = (255, 215, 0, 255) if self.is_super else (180, 180, 255, 255)
        renderer.fill_rect((x - 3, y - 3, 6, 6))


flies = [Fly(), Fly(), Fly(is_super=True)]

# --- НОГИ ---
LEG_ATTACH = [3, 4, 15, 16]
SIDE = [-1, 1, 1, -1]
leg_targets = [[W // 2, H // 2] for _ in range(4)]
leg_current = [[W // 2, H // 2] for _ in range(4)]
leg_phase = [0.0] * 4
particles = []


def solve_ik(base, target, len1, len2, flip=1):
    dx, dy = target[0] - base[0], target[1] - base[1]
    d = math.hypot(dx, dy)
    d = min(max(d, 5), len1 + len2 - 1)
    a = math.atan2(dy, dx)
    cos_b = (len1 ** 2 + d ** 2 - len2 ** 2) / (2 * len1 * d)
    b = math.acos(max(-1, min(1, cos_b)))
    return [base[0] + math.cos(a - b * flip) * len1, base[1] + math.sin(a - b * flip) * len1]


tongue_len = 0
tongue_active = False
target_fly = None
lizard_speed = 0.0001  # Базовая скорость

clock = pygame.time.Clock()
running = True

pygame.mouse.set_visible(False)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.MOUSEBUTTONDOWN: tongue_active = True

    mx, my = pygame.mouse.get_pos()
    t = pygame.time.get_ticks() * 0.001

    # 1. ДВИЖЕНИЕ ГОЛОВЫ
    speed_v = math.hypot(mx - segments[0][0], my - segments[0][1])
    wave_offset += speed_v * 0.05
    target = [mx + math.sin(t * 2.5) * 15, my + math.cos(t * 2) * 10]
    segments[0] = lerp(segments[0], target, lizard_speed)

    for i in range(1, NUM_SEG):
        l_wave = math.sin(wave_offset * 0.4 - i * 0.3) * (speed_v * 0.12)
        dx, dy = segments[i - 1][0] - segments[i][0], segments[i - 1][1] - segments[i][1]
        ang = math.atan2(dy, dx)
        segments[i] = [segments[i - 1][0] - math.cos(ang) * SEG_DIST + math.cos(ang + 1.57) * l_wave * 0.05,
                       segments[i - 1][1] - math.sin(ang) * SEG_DIST + math.sin(ang + 1.57) * l_wave * 0.05]

    # 2. МУХИ И ЯЗЫК
    for f in flies: f.update(segments[0])

    if tongue_active:
        if target_fly is None:
            for f in flies:
                if math.hypot(f.pos[0] - mx, f.pos[1] - my) < 60: target_fly = f; break
        aim = target_fly.pos if target_fly else [mx, my]
        dist_t = math.hypot(aim[0] - segments[0][0], aim[1] - segments[0][1])
        tongue_len = lerp(tongue_len, dist_t, 0.5)
        if tongue_len > dist_t - 8:
            tongue_active = False
            if target_fly and math.hypot(tongue_len - dist_t, 0) < 15: target_fly.is_caught = True
    else:
        tongue_len = lerp(tongue_len, 0, 0.2)
        if tongue_len < 2:
            for f in flies:
                if f.is_caught:
                    swallowed_foods.append(0.0)
                    if f.is_super: lizard_speed = 0.15  # Ускорение!
                    f.__init__(is_super=f.is_super)
            target_fly = None

    lizard_speed = lerp(lizard_speed, 0.08, 0.01)  # Плавное возвращение к норме

    # 3. ШАГИ
    for p_idx, pair in enumerate([[0, 3], [1, 2]]):
        can_step = not any(leg_phase[p] > 0 for p in [[1, 2], [0, 3]][p_idx])
        for i in pair:
            bx, by = segments[LEG_ATTACH[i]]
            ang = math.atan2(segments[LEG_ATTACH[i] - 1][1] - by, segments[LEG_ATTACH[i] - 1][0] - bx)
            ix, iy = bx + math.cos(ang + 1.57 * SIDE[i]) * 35 + math.cos(ang) * 20, by + math.sin(
                ang + 1.57 * SIDE[i]) * 35 + math.sin(ang) * 20
            if math.hypot(ix - leg_targets[i][0], iy - leg_targets[i][1]) > 55 and can_step:
                leg_phase[i] = 0.1;
                leg_targets[i] = [ix, iy]
                particles.append([[ix, iy], 1.0])
            if leg_phase[i] > 0:
                leg_phase[i] += 0.15
                leg_current[i] = lerp(leg_current[i], leg_targets[i], leg_phase[i])
                if leg_phase[i] >= 1.0: leg_phase[i] = 0

    # 4. ОТРИСОВКА
    rend.draw_color = (15, 18, 15, 255);
    rend.clear()
    for p in particles[:]:
        p[1] -= 0.05
        if p[1] <= 0:
            particles.remove(p)
        else:
            rend.draw_color = (100, 90, 70, int(p[1] * 255))
            rend.fill_rect((int(p[0][0]), int(p[0][1]), 3, 3))

    # Лапы
    for i in range(4):
        seg = segments[LEG_ATTACH[i]]
        ang_b = math.atan2(segments[LEG_ATTACH[i] - 1][1] - seg[1], segments[LEG_ATTACH[i] - 1][0] - seg[0])
        sh = [seg[0] + math.cos(ang_b + 1.57 * SIDE[i]) * 15, seg[1] + math.sin(ang_b + 1.57 * SIDE[i]) * 15]
        knee = solve_ik(sh, leg_current[i], 20, 20, SIDE[i])
        c = int(100 + math.sin(t * 4 + i) * 50);
        rend.draw_color = (40, c, 60, 255)
        for s_pt, e_pt, sz in [(sh, knee, 8), (knee, leg_current[i], 6)]:
            for step in range(5):
                pos = lerp(s_pt, e_pt, step / 4);
                rend.fill_rect((int(pos[0] - sz // 2), int(pos[1] - sz // 2), sz, sz))

    # Язык
    if tongue_len > 2:
        ang_t = math.atan2(my - segments[0][1], mx - segments[0][0])
        if target_fly: ang_t = math.atan2(target_fly.pos[1] - segments[0][1], target_fly.pos[0] - segments[0][0])
        tx, ty = segments[0][0] + math.cos(ang_t) * tongue_len, segments[0][1] + math.sin(ang_t) * tongue_len
        rend.draw_color = (255, 100, 150, 255);
        rend.draw_line((int(segments[0][0]), int(segments[0][1])), (int(tx), int(ty)))
        rend.fill_rect((int(tx - 6), int(ty - 6), 12, 12))
        if target_fly and target_fly.is_caught: target_fly.pos = [tx, ty]

    # Тело
    for p_idx in range(len(swallowed_foods) - 1, -1, -1):
        swallowed_foods[p_idx] += 0.18
        if swallowed_foods[p_idx] >= NUM_SEG: swallowed_foods.pop(p_idx)

    for i in range(NUM_SEG):
        size = int(12 - i * 0.4) if i < 16 else int(6 - (i - 16) * 0.3)
        bright = 0
        for f_p in swallowed_foods:
            if abs(i - f_p) < 2.5:
                v = (1 - abs(i - f_p) / 2.5);
                size += int(7 * v);
                bright += int(60 * v)
        c = int(100 + math.sin(t * 4 + i * 0.3) * 50)
        rend.draw_color = (min(255, 40 + bright), min(255, c + bright), min(255, 60 + bright), 255)
        rend.fill_rect((int(segments[i][0] - size), int(segments[i][1] - size), size * 2, size * 2))
        if i == 0:
            rend.draw_color = (255, 255, 255, 255)
            for side in [-1, 1]:
                ex = segments[0][0] + math.cos(
                    math.atan2(segments[0][1] - segments[1][1], segments[0][0] - segments[1][0]) + 0.8 * side) * 8
                ey = segments[0][1] + math.sin(
                    math.atan2(segments[0][1] - segments[1][1], segments[0][0] - segments[1][0]) + 0.8 * side) * 8
                rend.fill_rect((int(ex - 3), int(ey - 3), 6, 6))
                rend.draw_color = (0, 0, 0, 255)
                l_a = math.atan2(my - ey, mx - ex);
                rend.fill_rect((int(ex + math.cos(l_a) * 2 - 1), int(ey + math.sin(l_a) * 2 - 1), 3, 3))
                rend.draw_color = (255, 255, 255, 255)

    for f in flies: f.draw(rend)
    rend.present()
    clock.tick(60)
pygame.quit()
