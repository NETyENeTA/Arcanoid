import pygame
from pygame._sdl2 import Window, Renderer
import math

# Настройки
WIDTH, HEIGHT = 800, 600
CENTER = (WIDTH // 2, HEIGHT // 2)
FPS = 60

pygame.init()
win = Window("SDL2 Solar System", size=(WIDTH, HEIGHT))
rend = Renderer(win)

# Данные планет: [радиус орбиты, скорость, радиус сферы, цвет, текущий угол]
planets = [
    {"dist": 0, "speed": 0, "radius": 40, "color": (255, 200, 0), "angle": 0},  # Солнце
    {"dist": 150, "speed": 0.02, "radius": 15, "color": (50, 150, 255), "angle": 0},  # Земля
    {"dist": 250, "speed": 0.01, "radius": 20, "color": (200, 50, 50), "angle": math.pi}  # Марс
]

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    rend.draw_color = (10, 10, 20)
    rend.clear()

    # 1. Вычисляем 3D позиции и сохраняем для сортировки
    render_list = []
    for p in planets:
        p["angle"] += p["speed"]

        # 3D координаты (вращение в плоскости XZ)
        x = math.cos(p["angle"]) * p["dist"]
        y = math.sin(p["angle"]) * 0.3 * p["dist"]  # Наклон орбиты для "объема"
        z = math.sin(p["angle"]) * p["dist"]  # Глубина

        # Простая проекция (перспектива)
        scale = 400 / (400 + z)
        screen_x = int(CENTER[0] + x * scale)
        screen_y = int(CENTER[1] + y * scale)
        screen_radius = max(1, int(p["radius"] * scale))

        render_list.append({
            "pos": (screen_x, screen_y),
            "radius": screen_radius,
            "color": p["color"],
            "z": z
        })

    # 2. Сортировка по Z (художника алгоритм), чтобы дальние объекты были снизу
    render_list.sort(key=lambda obj: obj["z"], reverse=True)

    # 3. Рисование
    for obj in render_list:
        rend.draw_color = obj["color"]
        # В SDL2 Renderer нет рисования круга, используем закрашенный прямоугольник
        # или рисуем "точку" через rect для простоты примера
        rect = pygame.Rect(obj["pos"][0] - obj["radius"],
                           obj["pos"][1] - obj["radius"],
                           obj["radius"] * 2, obj["radius"] * 2)
        rend.fill_rect(rect)

    rend.present()
    clock.tick(FPS)

pygame.quit()
