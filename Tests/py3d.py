import pygame
import pygame._sdl2.video as video
import math

# --- КОНФИГУРАЦИЯ ---
RES = WIDTH, HEIGHT = 1600, 900
FPS = 165
FOV = math.pi / 2  # 60 градусов
NUM_RAYS = 600  # Количество лучей (полосок)
MOUSE_SENS = 0.0015
PLAYER_SPEED = 0.05
PITCH_LIMIT = 1400  # Наклон головы

# Карта: 1 - стена, 0 - пусто
MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


class DoomEngine:
    def __init__(self):
        pygame.init()
        # Инициализация окна SDL2
        self.win = video.Window("DOOM CE SDL2 - DDA Edition", size=RES)
        self.renderer = video.Renderer(self.win)
        self.clock = pygame.time.Clock()

        # Состояние игрока
        self.x, self.y = 1.5, 1.5
        self.angle = 0
        self.pitch = 0  # Вертикальный обзор

        # Коэффициент проекции для нормализации высоты стен
        self.proj_coeff = (WIDTH / 2) / math.tan(FOV / 2)
        self.scale = WIDTH / NUM_RAYS

        pygame.mouse.set_relative_mode(True)

    def handle_input(self):
        # Мышь
        rel_x, rel_y = pygame.mouse.get_rel()
        self.angle += rel_x * MOUSE_SENS
        self.pitch = max(-PITCH_LIMIT, min(PITCH_LIMIT, self.pitch - rel_y * 2))

        # Клавиатура
        keys = pygame.key.get_pressed()
        sin_a, cos_a = math.sin(self.angle), math.cos(self.angle)
        dx, dy = 0, 0

        if keys[pygame.K_w]: dx += cos_a; dy += sin_a
        if keys[pygame.K_s]: dx -= cos_a; dy -= sin_a
        if keys[pygame.K_a]: dx += sin_a; dy -= cos_a
        if keys[pygame.K_d]: dx -= sin_a; dy += cos_a

        if dx != 0 or dy != 0:
            norm = PLAYER_SPEED / math.sqrt(dx ** 2 + dy ** 2)
            dx, dy = dx * norm, dy * norm

        # Коллизии
        if MAP[int(self.y)][int(self.x + dx * 2)] == 0: self.x += dx
        if MAP[int(self.y + dy * 2)][int(self.x)] == 0: self.y += dy

    def draw(self):
        # Небо
        self.renderer.draw_color = (10, 10, 25, 255)
        self.renderer.clear()

        # Пол
        self.renderer.draw_color = (30, 30, 30, 255)
        self.renderer.fill_rect((0, HEIGHT // 2 + self.pitch, WIDTH, HEIGHT))

        # Raycasting DDA
        for r in range(NUM_RAYS):
            # Нормализация FOV: лучи распределяются по плоскости экрана, а не по углу
            screen_x = 2 * r / NUM_RAYS - 1
            ray_angle = self.angle + math.atan(screen_x * math.tan(FOV / 2))

            sin_a, cos_a = math.sin(ray_angle), math.cos(ray_angle)

            # Настройка DDA
            map_x, map_y = int(self.x), int(self.y)
            delta_x = abs(1 / cos_a) if cos_a != 0 else 1e30
            delta_y = abs(1 / sin_a) if sin_a != 0 else 1e30

            if cos_a < 0:
                step_x, side_x = -1, (self.x - map_x) * delta_x
            else:
                step_x, side_x = 1, (map_x + 1.0 - self.x) * delta_x
            if sin_a < 0:
                step_y, side_y = -1, (self.y - map_y) * delta_y
            else:
                step_y, side_y = 1, (map_y + 1.0 - self.y) * delta_y

            # Прыжки по сетке
            hit, side = 0, 0
            while not hit:
                if side_x < side_y:
                    side_x += delta_x
                    map_x += step_x
                    side = 0
                else:
                    side_y += delta_y
                    map_y += step_y
                    side = 1
                if MAP[map_y][map_x] > 0: hit = 1

            # Дистанция и фикс "рыбьего глаза"
            dist = (side_x - delta_x) if side == 0 else (side_y - delta_y)
            dist *= math.cos(ray_angle - self.angle)

            # Отрисовка полоски
            wall_h = self.proj_coeff / (dist + 0.0001)

            # Освещение
            color = int(255 / (1 + dist * dist * 0.02))
            if side == 1: color //= 1.4  # Тень на одной стороне стен

            self.renderer.draw_color = (0, color, color // 2, 255)

            # Позиция с учетом наклона головы
            y_pos = (HEIGHT // 2 - wall_h // 2) + self.pitch
            rect = (r * self.scale, y_pos, self.scale + 1, wall_h)
            self.renderer.fill_rect(rect)

        self.renderer.present()

    def run(self):
        global NUM_RAYS
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

                if event.type == pygame.MOUSEWHEEL:
                    temp = NUM_RAYS + int(event.y) * 10
                    if WIDTH > temp > 0:
                        NUM_RAYS += int(event.y) * 10
                        self.scale = WIDTH / NUM_RAYS

            self.handle_input()
            self.draw()
            self.clock.tick(FPS)
            self.win.title = f"{self.clock.get_fps()} fps"


if __name__ == "__main__":
    DoomEngine().run()
