import pygame
from pygame._sdl2 import Window, Renderer
import math
import random

pygame.init()
W, H = 800, 600
win = Window("Lizard: Eyes & Fixed Lerp", size=(W, H))
rend = Renderer(win)


# --- ФУНКЦИЯ LERP (Универсальная) ---
def lerp(a, b, f):
    if isinstance(a, (list, tuple)):
        return [a[i] + f * (b[i] - a[i]) for i in range(len(a))]
    return a + f * (b - a)


# --- ПАРАМЕТРЫ ТЕЛА ---
NUM_SEG = 26
SEG_DIST = 10
segments = [[W // 2, H // 2] for _ in range(NUM_SEG)]
wave_offset = 0.0
food_pos = -1.0

# --- НОГИ ---
LEG_ATTACH = [3, 4, 16, 17]
SIDE = [-1, 1, 1, -1]
leg_targets = [[W // 2, H // 2] for _ in range(4)]
leg_current = [[W // 2, H // 2] for _ in range(4)]
leg_phase = [0.0] * 4

# --- ЯЗЫК И МУХА ---
tongue_len = 0
tongue_active = False
fly_pos = [random.randint(100, W - 100), random.randint(100, H - 100)]
fly_vel = [0.0, 0.0]


def solve_ik(base_x, base_y, target_x, target_y, len1, len2, flip=1):
    dx, dy = target_x - base_x, target_y - base_y
    d = math.hypot(dx, dy)
    d = min(max(d, 5), len1 + len2 - 1)
    a = math.atan2(dy, dx)
    cos_b = (len1 ** 2 + d ** 2 - len2 ** 2) / (2 * len1 * d)
    b = math.acos(max(-1, min(1, cos_b)))
    return (base_x + math.cos(a - b * flip) * len1, base_y + math.sin(a - b * flip) * len1)


clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.MOUSEBUTTONDOWN: tongue_active = True

    mx, my = pygame.mouse.get_pos()
    t = pygame.time.get_ticks() * 0.001

    # 1. ГОЛОВА
    speed_vec = math.hypot(mx - segments[0][0], my - segments[0][1])
    wave_offset += speed_vec * 0.05
    target = [mx + math.sin(t * 2) * 20, my + math.cos(t * 1.5) * 15]
    segments[0] = lerp(segments[0], target, 0.1)

    # 2. ТЕЛО
    for i in range(1, NUM_SEG):
        lateral_wave = math.sin(wave_offset * 0.4 - i * 0.3) * (speed_vec * 0.15)
        dx, dy = segments[i - 1][0] - segments[i][0], segments[i - 1][1] - segments[i][1]
        ang = math.atan2(dy, dx)
        off_x, off_y = math.cos(ang + math.pi / 2) * lateral_wave, math.sin(ang + math.pi / 2) * lateral_wave
        segments[i] = [segments[i - 1][0] - math.cos(ang) * SEG_DIST + off_x * 0.05,
                       segments[i - 1][1] - math.sin(ang) * SEG_DIST + off_y * 0.05]

    # 3. ЕДА И МУХА
    if food_pos >= 0:
        food_pos += 0.2
        if food_pos >= NUM_SEG: food_pos = -1.0

    dist_f = math.hypot(fly_pos[0] - segments[0][0], fly_pos[1] - segments[0][1])
    if dist_f < 120:
        fly_vel[0] += (fly_pos[0] - segments[0][0]) * 0.04
        fly_vel[1] += (fly_pos[1] - segments[0][1]) * 0.04
    fly_pos[0] = (fly_pos[0] + fly_vel[0]) % W
    fly_pos[1] = (fly_pos[1] + fly_vel[1]) % H
    fly_vel[0] *= 0.9;
    fly_vel[1] *= 0.9

    # 4. ЯЗЫК
    if tongue_active:
        dist_t = math.hypot(mx - segments[0][0], my - segments[0][1])
        tongue_len = lerp(tongue_len, dist_t, 0.5)
        if tongue_len > dist_t - 10:
            tongue_active = False
            if math.hypot(mx - fly_pos[0], my - fly_pos[1]) < 40:
                food_pos = 0.0
                fly_pos = [random.randint(100, W - 100), random.randint(100, H - 100)]
    else:
        tongue_len = lerp(tongue_len, 0, 0.2)

    # 5. НОГИ
    pairs = [[0, 3], [1, 2]]
    for p_idx, pair in enumerate(pairs):
        can_step = not any(leg_phase[p] > 0 for p in pairs[(p_idx + 1) % 2])
        for i in pair:
            bx, by = segments[LEG_ATTACH[i]]
            ang = math.atan2(segments[LEG_ATTACH[i] - 1][1] - by, segments[LEG_ATTACH[i] - 1][0] - bx)
            ix = bx + math.cos(ang + math.pi / 2 * SIDE[i]) * 35 + math.cos(ang) * 20
            iy = by + math.sin(ang + math.pi / 2 * SIDE[i]) * 35 + math.sin(ang) * 20
            if math.hypot(ix - leg_targets[i][0], iy - leg_targets[i][1]) > 50 and can_step:
                leg_phase[i] = 0.1;
                leg_targets[i] = [ix, iy]
            if leg_phase[i] > 0:
                leg_phase[i] += 0.15
                leg_current[i] = lerp(leg_current[i], leg_targets[i], leg_phase[i])
                if leg_phase[i] >= 1.0: leg_phase[i] = 0

    # 6. ОТРИСОВКА
    rend.draw_color = (15, 18, 15, 255);
    rend.clear()

    # ЛАПЫ (Переливающиеся квадраты)
    for i in range(4):
        seg_idx = LEG_ATTACH[i]
        bx, by = segments[seg_idx]
        ang_head = math.atan2(segments[seg_idx - 1][1] - by, segments[seg_idx - 1][0] - bx)
        sh_x, sh_y = bx + math.cos(ang_head + math.pi / 2 * SIDE[i]) * 15, by + math.sin(
            ang_head + math.pi / 2 * SIDE[i]) * 15
        knee = solve_ik(sh_x, sh_y, leg_current[i][0], leg_current[i][1], 20, 20, SIDE[i])

        c = int(100 + math.sin(t * 4 + seg_idx * 0.3) * 50)
        rend.draw_color = (40, c, 60, 255)
        # Бедро и Голень
        for start, end, s in [((sh_x, sh_y), knee, 8), (knee, leg_current[i], 6)]:
            for step in range(5):
                pos = lerp(start, end, step / 4)
                rend.fill_rect((int(pos[0] - s // 2), int(pos[1] - s // 2), s, s))

    # ЯЗЫК
    if tongue_len > 5:
        at = math.atan2(my - segments[0][1], mx - segments[0][0])
        tx, ty = segments[0][0] + math.cos(at) * tongue_len, segments[0][1] + math.sin(at) * tongue_len
        rend.draw_color = (255, 100, 150, 255);
        rend.draw_line((int(segments[0][0]), int(segments[0][1])), (int(tx), int(ty)))
        rend.fill_rect((int(tx - 6), int(ty - 6), 12, 12))

    # ТЕЛО
    for i in range(NUM_SEG):
        size = int(12 - i * 0.4) if i < 15 else int(6 - (i - 15) * 0.3)
        if food_pos >= 0 and abs(i - food_pos) < 2:
            size += int(6 * (1 - abs(i - food_pos) / 2))
        c = int(100 + math.sin(t * 4 + i * 0.3) * 50)
        rend.draw_color = (40, c, 60, 255)
        rend.fill_rect((int(segments[i][0] - size), int(segments[i][1] - size), size * 2, size * 2))

        # ГЛАЗА (только на голове i=0)
        if i == 0:
            rend.draw_color = (255, 255, 255, 255)
            for side in [-1, 1]:
                eye_ang = math.atan2(segments[0][1] - segments[1][1], segments[0][0] - segments[1][0])
                ex = segments[0][0] + math.cos(eye_ang + 0.8 * side) * 8
                ey = segments[0][1] + math.sin(eye_ang + 0.8 * side) * 8
                rend.fill_rect((int(ex - 3), int(ey - 3), 6, 6))
                # Зрачки смотрят на мышь
                rend.draw_color = (0, 0, 0, 255)
                look_ang = math.atan2(my - ey, mx - ex)
                rend.fill_rect((int(ex + math.cos(look_ang) * 2 - 1), int(ey + math.sin(look_ang) * 2 - 1), 3, 3))
                rend.draw_color = (255, 255, 255, 255)

    rend.draw_color = (180, 180, 255, 255);
    rend.fill_rect((int(fly_pos[0] - 3), int(fly_pos[1] - 3), 6, 6))
    rend.present()
    clock.tick(60)
pygame.quit()
