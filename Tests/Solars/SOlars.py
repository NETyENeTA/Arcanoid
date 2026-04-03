import pygame
from pygame._sdl2 import Window, Renderer, Texture
import math
import random

# Настройки
WIDTH, HEIGHT = 1600, 900
pygame.init()
font = pygame.font.SysFont("Arial", 22, bold=True)

win = Window("Solar System - Full Edition", size=(WIDTH, HEIGHT))
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


# --- ДАННЫЕ ВСЕХ ПЛАНЕТ И СПУТНИКОВ ---
bodies_info = [
    {"n": "SUN", "p": 1000, "r": 90, "orb": 0, "s": 0, "c": (255, 210, 50)},
    {"n": "MERCURY", "p": 80, "r": 8, "orb": 280, "s": 0.03, "c": (170, 170, 170)},
    {"n": "VENUS", "p": 120, "r": 16, "orb": 450, "s": 0.02, "c": (240, 230, 180)},
    {"n": "EARTH", "p": 150, "r": 18, "orb": 650, "s": 0.015, "c": (60, 160, 255),
     "moons": [{"n": "Moon", "p": 40, "r": 5, "orb": 45, "s": 0.08, "c": (200, 200, 200)}]},
    {"n": "MARS", "p": 120, "r": 12, "orb": 850, "s": 0.012, "c": (255, 80, 50)},
    {"n": "JUPITER", "p": 400, "r": 55, "orb": 1200, "s": 0.007, "c": (220, 180, 140),
     "moons": [{"n": "Io", "p": 35, "r": 4, "orb": 85, "s": 0.06, "c": (255, 255, 100)},
               {"n": "Europa", "p": 35, "r": 4, "orb": 110, "s": 0.04, "c": (200, 230, 255)}]},
    {"n": "SATURN", "p": 350, "r": 45, "orb": 1600, "s": 0.005, "c": (210, 200, 150), "rings": True},
    {"n": "URANUS", "p": 250, "r": 30, "orb": 2000, "s": 0.003, "c": (160, 240, 240)},
    {"n": "NEPTUNE", "p": 250, "r": 29, "orb": 2400, "s": 0.002, "c": (80, 100, 255)},
]

# Генерация объектов и текстур
planets = []
for b in bodies_info:
    t_surf = font.render(b["n"], True, b["c"])
    b["t_tex"] = Texture.from_surface(rend, t_surf)
    b["t_tex"].alpha = 0
    b["t_size"] = t_surf.get_size()
    b["hud_alpha"] = 0.0

    p_dict = {**b, "pts": gen_sphere(b["p"], b["r"], b["c"]), "angle": random.random() * 6.28}

    if "moons" in b:
        for m in b["moons"]:
            m["pts"] = gen_sphere(m["p"], m["r"], m["c"])
            m["angle"] = random.random() * 6.28
            # Текстуры для названий лун
            m_surf = font.render(m["n"], True, m["c"])
            m["t_tex"] = Texture.from_surface(rend, m_surf)
            m["t_size"] = m_surf.get_size()
            m["hud_alpha"] = 0.0

    if "rings" in b:
        p_dict["ring_pts"] = [[math.cos(a) * r, random.uniform(-1, 1), math.sin(a) * r, (180, 170, 150)]
                              for r, a in [(random.uniform(70, 130), random.uniform(0, 6.28)) for _ in range(500)]]
    planets.append(p_dict)

stars = [[random.randint(-15000, 15000) for _ in range(3)] for _ in range(3000)]

# Состояние
cam_x, cam_y, cam_z = 0, 1000, -4500
vel_x = vel_y = vel_z = 0.0
ACCEL, FRICTION = 10.0, 0.95
clock = pygame.time.Clock()

while True:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); exit()

    # Look-at Sun
    dx, dy, dz = -cam_x, -cam_y, -cam_z
    yaw = math.atan2(dx, dz)
    pitch = math.atan2(dy, math.sqrt(dx ** 2 + dz ** 2))

    # Controls
    keys = pygame.key.get_pressed()
    warp = keys[pygame.K_LSHIFT]
    cur_acc = ACCEL * 15.0 if warp else ACCEL
    sy, cy, sp, cp = math.sin(yaw), math.cos(yaw), math.sin(pitch), math.cos(pitch)

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
    shake = (random.uniform(-1, 1) * speed * 0.005) if warp else 0

    rend.draw_color = (2, 2, 8, 255);
    rend.clear()
    fov = 950 + (speed * 0.05)


    def project(tx, ty, tz):
        rx = tx * cy - tz * sy
        rz = tx * sy + tz * cy
        ry = ty * cp - rz * sp
        rz = ty * sp + rz * cp
        if rz <= 10: return None
        f = fov / rz
        return (int(rx * f + WIDTH // 2 + shake), int(ry * f + HEIGHT // 2 + shake), rz, f)


    # Stars
    for sx, sy_s, sz in stars:
        p1 = project(sx - cam_x, sy_s - cam_y, sz - cam_z)
        if p1:
            tail = 0.0001 + (speed * 0.0001)
            p2 = project(sx - cam_x - vel_x * tail, sy_s - cam_y - vel_y * tail, sz - cam_z - vel_z * tail)
            sh = int(min(255, 140 + speed * 0.05))
            rend.draw_color = (sh, sh, 255, 255)
            if p2:
                rend.draw_line((p1[0], p1[1]), (p2[0], p2[1]))
            else:
                rend.fill_rect((p1[0], p1[1], 1, 1))

    render_queue = []
    hud_elements = []

    for p in planets:
        p["angle"] += p["s"] * 0.3
        bx, bz = math.cos(p["angle"]) * p["orb"], math.sin(p["angle"]) * p["orb"]

        # --- PLANET HUD ---
        dist_p = math.sqrt((bx - cam_x) ** 2 + (0 - cam_y) ** 2 + (bz - cam_z) ** 2)
        p["hud_alpha"] += ((1.0 if dist_p < 3000 else 0.0) - p["hud_alpha"]) * 0.1
        if p["hud_alpha"] > 0.01:
            pr = project(bx - cam_x, -cam_y, bz - cam_z)
            if pr: hud_elements.append((p["t_tex"], pr, p["t_size"], p["hud_alpha"], p["c"], p["r"] * (fov / pr[2])))

        # Planet Body
        for px, py, pz, col in p["pts"]:
            proj = project((px + bx) - cam_x, py - cam_y, (pz + bz) - cam_z)
            if proj: render_queue.append((*proj, col, 2))

        # Rings
        if "ring_pts" in p:
            for rx, ry, rz_p, col in p["ring_pts"]:
                proj = project((rx + bx) - cam_x, ry - cam_y, (rz_p + bz) - cam_z)
                if proj: render_queue.append((*proj, col, 1))

        # --- MOONS ---
        if "moons" in p:
            for m in p["moons"]:
                m["angle"] += m["s"] * 0.6
                mx, mz = bx + math.cos(m["angle"]) * m["orb"], bz + math.sin(m["angle"]) * m["orb"]

                # Moon HUD
                dist_m = math.sqrt((mx - cam_x) ** 2 + (0 - cam_y) ** 2 + (mz - cam_z) ** 2)
                m["hud_alpha"] += ((1.0 if dist_m < 800 else 0.0) - m["hud_alpha"]) * 0.1
                if m["hud_alpha"] > 0.01:
                    pm = project(mx - cam_x, -cam_y, mz - cam_z)
                    if pm: hud_elements.append(
                        (m["t_tex"], pm, m["t_size"], m["hud_alpha"], m["c"], m["r"] * (fov / pm[2])))

                # Moon Body
                for mpx, mpy, mpz, mcol in m["pts"]:
                    proj = project((mpx + mx) - cam_x, mpy - cam_y, (mpz + mz) - cam_z)
                    if proj: render_queue.append((*proj, mcol, 1.5))

    # Sort & Draw
    render_queue.sort(key=lambda x: x[2], reverse=True)
    for sx, sy, rz, f, col, b_size in render_queue:
        size = max(1, int(b_size * f * 1.5))
        sh = max(0.1, min(1.0, 5000 / (rz + 2500)))
        rend.draw_color = (int(col[0] * sh), int(col[1] * sh), int(col[2] * sh), 255)
        rend.fill_rect((sx, sy, size, size))

    # Draw Animated HUD
    for tex, pr, t_size, alpha, col, p_size_px in hud_elements:
        tex.alpha = int(alpha * 255)
        rend.draw_color = (col[0], col[1], col[2], int(alpha * 180))
        off_y = 60 + (1.0 - alpha) * 30

        # Line & Frame
        rend.draw_line((pr[0], pr[1]), (pr[0], pr[1] - int(off_y) + 10))
        r, L = int(p_size_px) + 10, 15
        rend.draw_line((pr[0] - r, pr[1] - r), (pr[0] - r + L, pr[1] - r))
        rend.draw_line((pr[0] - r, pr[1] - r), (pr[0] - r, pr[1] - r + L))
        rend.draw_line((pr[0] + r, pr[1] + r), (pr[0] + r - L, pr[1] + r))
        rend.draw_line((pr[0] + r, pr[1] + r), (pr[0] + r, pr[1] + r - L))

        rend.blit(tex, pygame.Rect(pr[0] - t_size[0] // 2, pr[1] - int(off_y), t_size[0], t_size[1]))

    rend.present()
