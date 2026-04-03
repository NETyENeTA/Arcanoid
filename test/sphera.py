import pygame
from pygame._sdl2 import Window, Renderer, Texture
import math

# Настройки
WIDTH, HEIGHT = 800, 600
NUM_POINTS = 600  # 600
SPHERE_RADIUS = 200
PUSH_RADIUS = 80 # 80
PUSH_STRENGTH = 50 # 50

pygame.init()
win = Window("SDL2 Sphere", size=(WIDTH, HEIGHT))
rend = Renderer(win)

# Генерация точек (Фибоначчи)
points = []
phi = math.pi * (3. - math.sqrt(5.))
for i in range(NUM_POINTS):
    y = 1 - (i / (NUM_POINTS - 1)) * 2
    rad = math.sqrt(1 - y * y)
    theta = phi * i
    points.append([math.cos(theta) * rad * SPHERE_RADIUS,
                   y * SPHERE_RADIUS,
                   math.sin(theta) * rad * SPHERE_RADIUS])

angle_x = angle_y = 0
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mx, my = pygame.mouse.get_pos()
    rend.draw_color = (10, 15, 30, 255)
    rend.clear()

    angle_x += 0.005
    angle_y += 0.01

    # Проекция и расчет
    transformed = []
    for x, y, z in points:
        # Вращение Y
        nx = x * math.cos(angle_y) + z * math.sin(angle_y)
        nz = -x * math.sin(angle_y) + z * math.cos(angle_y)
        # Вращение X
        ny = y * math.cos(angle_x) - nz * math.sin(angle_x)
        nz = y * math.sin(angle_x) + nz * math.cos(angle_x)

        sx, sy = nx + WIDTH // 2, ny + HEIGHT // 2

        # Смещение ТОЛЬКО для передних точек (nz > 0)
        if nz > 0:
            dx, dy = sx - mx, sy - my
            dist = math.hypot(dx, dy)
            if dist < PUSH_RADIUS and dist > 0:
                force = (1 - dist / PUSH_RADIUS) * PUSH_STRENGTH
                sx += (dx / dist) * force
                sy += (dy / dist) * force

        transformed.append((sx, sy, nz))

    # Сортировка для корректного наслоения
    transformed.sort(key=lambda p: p[2])

    # Отрисовка через SDL2 Renderer
    for x, y, z in transformed:
        size = int((z + SPHERE_RADIUS) / (2 * SPHERE_RADIUS) * 5) + 1
        brightness = int((z + SPHERE_RADIUS) / (2 * SPHERE_RADIUS) * 180) + 75

        rend.draw_color = (brightness // 2, brightness, 255, 255)
        # Рисуем точку как маленький квадрат (в SDL2 Renderer нет прямого Circle)
        rect = (int(x - size / 2), int(y - size / 2), size, size)
        rend.fill_rect(rect)

    rend.present()
    pygame.time.wait(10)

pygame.quit()
