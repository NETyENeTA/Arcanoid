import pygame
from pygame._sdl2 import Window, Renderer
import math

# Константы
WIDTH, HEIGHT = 800, 600
RADIUS = 180
ROWS, COLS = 24, 24  # Детализация сетки
PUSH_RADIUS = 90
PUSH_STRENGTH = 60

pygame.init()
win = Window("3D Wireframe Sphere", size=(WIDTH, HEIGHT))
rend = Renderer(win)

# 1. Генерация вершин сетки (сферические координаты)
vertices = []
for r in range(ROWS + 1):
    phi = math.pi * r / ROWS  # от 0 до pi
    for c in range(COLS):
        theta = 2 * math.pi * c / COLS  # от 0 до 2pi
        x = RADIUS * math.sin(phi) * math.cos(theta)
        y = RADIUS * math.cos(phi)
        z = RADIUS * math.sin(phi) * math.sin(theta)
        vertices.append([x, y, z])

angle_x = angle_y = 0


def rotate(v, ax, ay):
    x, y, z = v
    # Y-axis
    nx = x * math.cos(ay) + z * math.sin(ay)
    nz = -x * math.sin(ay) + z * math.cos(ay)
    # X-axis
    ny = y * math.cos(ax) - nz * math.sin(ax)
    nz = y * math.sin(ax) + nz * math.cos(ax)
    return [nx, ny, nz]


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    mx, my = pygame.mouse.get_pos()
    rend.draw_color = (5, 5, 15, 255)
    rend.clear()

    angle_x += 0.007
    angle_y += 0.012

    # 2. Трансформация всех вершин
    projected = []
    for v in vertices:
        rv = rotate(v, angle_x, angle_y)
        sx, sy = rv[0] + WIDTH // 2, rv[1] + HEIGHT // 2

        # Смещение только для передней части (z > 0)
        if rv[2] > 0:
            dx, dy = sx - mx, sy - my
            dist = math.hypot(dx, dy)
            if dist < PUSH_RADIUS and dist > 0:
                force = (1 - dist / PUSH_RADIUS) * PUSH_STRENGTH
                sx += (dx / dist) * force
                sy += (dy / dist) * force

        projected.append((int(sx), int(sy), rv[2]))

    # 3. Отрисовка ребер (линий)
    rend.draw_color = (0, 180, 255, 255)
    for r in range(ROWS):
        for c in range(COLS):
            i1 = r * COLS + c
            i2 = r * COLS + (c + 1) % COLS
            i3 = (r + 1) * COLS + c

            # Рисуем только если хотя бы одна точка спереди (для красоты)
            # Горизонтальные линии (параллели)
            # if projected[i1][2] > -50 or projected[i2][2] > -50:
            #     rend.draw_line((projected[i1][0], projected[i1][1]),
            #                    (projected[i2][0], projected[i2][1]))

            # Вертикальные линии (меридианы)
            if r < ROWS and (projected[i1][2] > -50 or projected[i3][2] > -50):
                rend.draw_line((projected[i1][0], projected[i1][1]),
                               (projected[i3][0], projected[i3][1]))\


    rend.present()
    pygame.time.wait(16)

pygame.quit()
