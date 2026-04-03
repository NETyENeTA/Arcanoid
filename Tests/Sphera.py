import pygame
import math
import random

# Инициализация pygame_ce
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Настройки сферы
NUM_POINTS = 400
SPHERE_RADIUS = 200
CENTER = (WIDTH // 2, HEIGHT // 2)
PUSH_RADIUS = 70  # Радиус влияния мышки
PUSH_STRENGTH = 40  # Сила смещения


def generate_sphere(n, r):
    points = []
    phi = math.pi * (3. - math.sqrt(5.))  # золотой угол
    for i in range(n):
        y = 1 - (i / float(n - 1)) * 2
        radius_at_y = math.sqrt(1 - y * y)
        theta = phi * i
        x = math.cos(theta) * radius_at_y
        z = math.sin(theta) * radius_at_y
        points.append([x * r, y * r, z * r])
    return points


def rotate_point(point, angle_x, angle_y):
    x, y, z = point
    # Поворот вокруг Y
    nx = x * math.cos(angle_y) + z * math.sin(angle_y)
    nz = -x * math.sin(angle_y) + z * math.cos(angle_y)
    # Поворот вокруг X
    ny = y * math.cos(angle_x) - nz * math.sin(angle_x)
    nz = y * math.sin(angle_x) + nz * math.cos(angle_x)
    return [nx, ny, nz]


points = generate_sphere(NUM_POINTS, SPHERE_RADIUS)
angle_x = angle_y = 0

running = True
while running:
    screen.fill((10, 10, 20))
    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Вращение
    angle_x += 0.005
    angle_y += 0.01

    # Обработка точек
    projected_points = []
    for p in points:
        # 1. Вращаем
        rotated = rotate_point(p, angle_x, angle_y)
        rx, ry, rz = rotated

        # 2. Считаем экранные координаты (центр + точка)
        screen_x = rx + CENTER[0]
        screen_y = ry + CENTER[1]

        # 3. Эффект смещения от мышки
        dx = screen_x - mx
        dy = screen_y - my
        dist = math.hypot(dx, dy)

        if dist < PUSH_RADIUS and dist > 0:
            force = (1 - dist / PUSH_RADIUS) * PUSH_STRENGTH
            screen_x += (dx / dist) * force
            screen_y += (dy / dist) * force

        projected_points.append((screen_x, screen_y, rz))

    # Сортировка по Z (глубине), чтобы ближние были сверху
    projected_points.sort(key=lambda p: p[2])

    # Отрисовка
    for x, y, z in projected_points:
        # Размер зависит от глубины Z
        size = int((z + SPHERE_RADIUS) / (2 * SPHERE_RADIUS) * 6) + 2
        # Цвет: чем ближе (больше Z), тем ярче
        brightness = int((z + SPHERE_RADIUS) / (2 * SPHERE_RADIUS) * 155) + 100
        pygame.draw.circle(screen, (brightness, 100, 255), (int(x), int(y)), size)

    pygame.display.flip()
    clock.tick(165)

pygame.quit()
