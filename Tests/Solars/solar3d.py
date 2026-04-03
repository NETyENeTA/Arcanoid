import pygame
from pygame._sdl2 import Window, Renderer
import math
import random

# Настройки
WIDTH, HEIGHT = 1600, 900
pygame.init()

win = Window("3D Solar System - Warp Drive & Moons", size=(WIDTH, HEIGHT))
rend = Renderer(win)
pygame.mouse.set_relative_mode(False)
rend.logical_size = (WIDTH, HEIGHT)


def gen_sphere(num_points, radius, color):
    pts = []
    phi = math.pi * (3. - math.sqrt(5.))
    for i in range(num_points):
        y = 1 - (i / (num_points - 1)) * 2
        rad = math.sqrt(1 - y * y)
        theta = phi * i
        pts.append([math.cos(theta) * rad * radius, y * radius, math.sin(theta) * rad * radius, color])
    return pts


# Данные системы: Планеты и их спутники
bodies_info = [
    {"n": "Sun", "p": 800, "r": 90, "orb": 0, "s": 0, "c": (255, 210, 50)},
    {"n": "Mercury", "p": 80, "r": 8, "orb": 280, "s": 0.03, "c": (170, 170, 170)},
    {"n": "Venus", "p": 120, "r": 16, "orb": 450, "s": 0.02, "c": (240, 230, 180)},
    {"n": "Earth", "p": 150, "r": 18, "orb": 650, "s": 0.015, "c": (60, 160, 255),
     "moons": [{"n": "Moon", "p": 40, "r": 4, "orb": 40, "s": 0.1, "c": (200, 200, 200)}]},
    {"n": "Mars", "p": 120, "r": 12, "orb": 850, "s": 0.012, "c": (255, 80, 50)},
    {"n": "Jupiter", "p": 400, "r": 55, "orb": 1200, "s": 0.007, "c": (220, 180, 140),
     "moons": [
         {"n": "Io", "p": 30, "r": 3, "orb": 80, "s": 0.08, "c": (255, 255, 100)},
         {"n": "Europa", "p": 30, "r": 3, "orb": 110, "s": 0.06, "c": (200, 230, 255)}
     ]},
    {"n": "Saturn", "p": 350, "r": 45, "orb": 1600, "s": 0.005, "c": (210, 200, 150), "rings": True},
    {"n": "Uranus", "p": 200, "r": 30, "orb": 2000, "s": 0.003, "c": (160, 240, 240)},
    {"n": "Neptune", "p": 200, "r": 29, "orb": 2400, "s": 0.002, "c": (80, 100, 255)},
]

# Генерация объектов
planets = []
for b in bodies_info:
    p_dict = {**b, "pts": gen_sphere(b["p"], b["r"], b["c"]), "angle": random.random() * 6.28}
    if "moons" in b:
        for m in b["moons"]:
            m["pts"] = gen_sphere(m["p"], m["r"], m["c"])
            m["angle"] = random.random() * 6.28
    if "rings" in b:
        p_dict["ring_pts"] = [[math.cos(a) * r, random.uniform(-1, 1), math.sin(a) * r, (180, 170, 150)]
                              for r, a in [(random.uniform(70, 130), random.uniform(0, 6.28)) for _ in range(600)]]
    planets.append(p_dict)

stars = [[random.randint(-12000, 12000) for _ in range(3)] for _ in range(3000)]

# Физика
cam_x, cam_y, cam_z = 0, 800, -4000
vel_x = vel_y = vel_z = 0.0
ACCEL, FRICTION = 100.0, 0.94
clock = pygame.time.Clock()

while True:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); exit()

    # Поворот к солнцу (0,0,0)
    dx, dy, dz = -cam_x, -cam_y, -cam_z
    yaw = math.atan2(dx, dz)
    pitch = math.atan2(dy, math.sqrt(dx ** 2 + dz ** 2))

    # Управление
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]: break

    warp = keys[pygame.K_LSHIFT]
    cur_acc = ACCEL * 10.0 if warp else ACCEL
    sy, cy = math.sin(yaw), math.cos(yaw)
    sp, cp = math.sin(pitch), math.cos(pitch)

    if keys[pygame.K_w]: vel_x += sy * cp * cur_acc; vel_y -= sp * cur_acc; vel_z += cy * cp * cur_acc
    if keys[pygame.K_s]: vel_x -= sy * cp * cur_acc; vel_y += sp * cur_acc; vel_z -= cy * cp * cur_acc
    if keys[pygame.K_a]: vel_x -= cy * cur_acc; vel_z += sy * cur_acc
    if keys[pygame.K_d]: vel_x += cy * cur_acc; vel_z -= sy * cur_acc
    if keys[pygame.K_LCTRL]: vel_y += cur_acc
    if keys[pygame.K_SPACE]: vel_y -= cur_acc

    cam_x += vel_x * dt;
    cam_y += vel_y * dt;
    cam_z += vel_z * dt
    vel_x *= FRICTION;
    vel_y *= FRICTION;
    vel_z *= FRICTION
    speed = math.sqrt(vel_x ** 2 + vel_y ** 2 + vel_z ** 2)

    # Рендеринг
    rend.draw_color = (2, 2, 8, 255);
    rend.clear()
    fov = 900 + (speed * 0.04)


    def project(tx, ty, tz):
        rx = tx * cy - tz * sy
        rz = tx * sy + tz * cy
        ry = ty * cp - rz * sp
        rz = ty * sp + rz * cp
        if rz <= 10: return None
        f = fov / rz
        return (int(rx * f + WIDTH // 2), int(ry * f + HEIGHT // 2), rz, f)


    # Звезды
    for sx, sy_s, sz in stars:
        p1 = project(sx - cam_x, sy_s - cam_y, sz - cam_z)
        if p1:
            tail = 0.0001 + (speed * 0.00008)
            p2 = project(sx - cam_x - vel_x * tail, sy_s - cam_y - vel_y * tail, sz - cam_z - vel_z * tail)
            shade = int(min(255, 160 + speed * 0.04))
            rend.draw_color = (shade, shade, 255, 255)
            if p2:
                rend.draw_line((p1[0], p1[1]), (p2[0], p2[1]))
            else:
                rend.fill_rect((p1[0], p1[1], 1, 1))

    # Сбор всех точек тел для сортировки
    render_queue = []
    for p in planets:
        p["angle"] += p["s"] * 0.3
        bx, bz = math.cos(p["angle"]) * p["orb"], math.sin(p["angle"]) * p["orb"]

        # Точки планеты
        for px, py, pz, col in p["pts"]:
            proj = project((px + bx) - cam_x, py - cam_y, (pz + bz) - cam_z)
            if proj: render_queue.append((*proj, col, 2))

        # Точки колец
        if "ring_pts" in p:
            for rx, ry, rz_p, col in p["ring_pts"]:
                proj = project((rx + bx) - cam_x, ry - cam_y, (rz_p + bz) - cam_z)
                if proj: render_queue.append((*proj, col, 1))

        # Спутники
        if "moons" in p:
            for m in p["moons"]:
                m["angle"] += m["s"] * 0.5
                mx = bx + math.cos(m["angle"]) * m["orb"]
                mz = bz + math.sin(m["angle"]) * m["orb"]
                for mpx, mpy, mpz, mcol in m["pts"]:
                    proj = project((mpx + mx) - cam_x, mpy - cam_y, (mpz + mz) - cam_z)
                    if proj: render_queue.append((*proj, mcol, 1.5))

    render_queue.sort(key=lambda x: x[2], reverse=True)
    for sx, sy, rz, f, col, b_size in render_queue:
        size = max(1, int(b_size * f * 1.5))
        sh = max(0.1, min(1.0, 5000 / (rz + 2500)))
        rend.draw_color = (int(col[0] * sh), int(col[1] * sh), int(col[2] * sh), 255)
        rend.fill_rect((sx, sy, size, size))

    rend.present()
