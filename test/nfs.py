import pygame
import math
import random

WIDTH, HEIGHT = 800, 600
FPS = 60
FOV = 400


def project(world_x, world_z, cam_x, cam_z, cam_angle):
    """ Настоящая 3D проекция с учетом поворота камеры """
    # 1. Смещение относительно игрока
    dx = world_x - cam_x
    dz = world_z - cam_z

    # 2. Вращение точки вокруг игрока (матрица поворота)
    # Инвертируем угол, чтобы мир вращался против движения игрока
    rx = dx * math.cos(-cam_angle) - dz * math.sin(-cam_angle)
    rz = dx * math.sin(-cam_angle) + dz * math.cos(-cam_angle)

    # 3. Отсечение (не рисуем то, что сзади)
    if rz < 10: return None

    # 4. Перспектива
    f = FOV / rz
    screen_x = WIDTH // 2 + rx * f
    screen_y = HEIGHT // 2 + 150 * f  # 150 - высота камеры
    return (int(screen_x), int(screen_y))


class Road:
    def __init__(self):
        self.points = []
        self.segments = 300
        self.seg_len = 200
        self.width = 400

        curr_x, curr_z = 0, 0
        angle = 0
        for i in range(self.segments):
            angle += math.sin(i * 0.1) * 0.05  # Плавные повороты
            curr_x += math.sin(angle) * self.seg_len
            curr_z += math.cos(angle) * self.seg_len

            # Вектор перпендикуляра для краев дороги
            perp_x = math.cos(angle) * self.width
            perp_z = -math.sin(angle) * self.width

            self.points.append({
                'L': (curr_x - perp_x, curr_z - perp_z),
                'R': (curr_x + perp_x, curr_z + perp_z),
                'C': (curr_x, curr_z)
            })

    def draw(self, screen, p_x, p_z, p_angle):
        # Рисуем только те сегменты, которые впереди (оптимизация)
        for i in range(len(self.points) - 1, 0, -1):
            p1 = self.points[i - 1]
            p2 = self.points[i]

            pts = [
                project(p1['L'][0], p1['L'][1], p_x, p_z, p_angle),
                project(p1['R'][0], p1['R'][1], p_x, p_z, p_angle),
                project(p2['R'][0], p2['R'][1], p_x, p_z, p_angle),
                project(p2['L'][0], p2['L'][1], p_x, p_z, p_angle)
            ]

            if all(pts):
                color = (50, 50, 50) if i % 2 == 0 else (60, 60, 60)
                pygame.draw.polygon(screen, color, pts)
                # Разметка
                pygame.draw.line(screen, (255, 255, 255), pts[0], pts[3], 2)
                pygame.draw.line(screen, (255, 255, 255), pts[1], pts[2], 2)


def draw_minimap(screen, player, bots, road):
    size = 150
    m = pygame.Surface((size, size))
    m.fill((30, 30, 30))
    scale = 0.005
    center = size // 2

    # Рисуем всю трассу на миникарте (целиком)
    map_pts = [(center + p['C'][0] * scale, center - p['C'][1] * scale) for p in road.points]
    if len(map_pts) > 1: pygame.draw.lines(m, (100, 100, 100), False, map_pts, 2)

    # Игрока и ботов
    for b in bots + [player]:
        px = center + b.x * scale
        pz = center - b.z * scale
        color = (255, 255, 0) if b == player else (255, 0, 0)
        pygame.draw.circle(m, color, (int(px), int(pz)), 3)

    screen.blit(m, (WIDTH - size - 10, 10))


class Car:
    def __init__(self, x, z, color):
        self.x, self.z = x, z
        self.color = color
        self.angle = 0
        self.speed = 0

    def update(self, dt, is_player=False):
        if is_player:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.speed += 1000 * dt
            elif keys[pygame.K_s]:
                self.speed -= 1000 * dt
            else:
                self.speed *= 0.97

            if keys[pygame.K_a]: self.angle -= 2 * dt
            if keys[pygame.K_d]: self.angle += 2 * dt

        self.x += math.sin(self.angle) * self.speed * dt
        self.z += math.cos(self.angle) * self.speed * dt


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    road = Road()
    player = Car(0, 0, (255, 255, 255))
    bots = [Car(random.randint(-200, 200), (i + 1) * 1000, (255, 0, 0)) for i in range(10)]

    while True:
        dt = clock.tick(FPS) / 1000.0
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return

        player.update(dt, True)

        screen.fill((100, 149, 237))  # Небо
        pygame.draw.rect(screen, (34, 139, 34), (0, HEIGHT // 2, WIDTH, HEIGHT // 2))  # Земля

        road.draw(screen, player.x, player.z, player.angle)

        for b in bots:
            # ИИ просто едет вперед по трассе
            b.speed = 400
            b.update(dt)
            p = project(b.x, b.z, player.x, player.z, player.angle)
            if p:
                dist = max(1, math.hypot(b.x - player.x, b.z - player.z))
                size = 15000 / dist
                pygame.draw.rect(screen, b.color, (p[0] - size / 2, p[1] - size, size, size))

        draw_minimap(screen, player, bots, road)
        pygame.display.flip()


main()
