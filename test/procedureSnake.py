import pygame
from pygame._sdl2 import Window, Renderer
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
win = Window("SDL2 Procedural Lizard", size=(WIDTH, HEIGHT))
rend = Renderer(win)

# Параметры ящерицы
NUM_SEGMENTS = 15
SEG_DISTANCE = 15  # Дистанция между сегментами
segments = [[WIDTH // 2, HEIGHT // 2] for _ in range(NUM_SEGMENTS)]


def move_lizard(target_x, target_y):
    # Голова следует за целью
    segments[0][0] = target_x
    segments[0][1] = target_y

    # Каждый сегмент тянется к предыдущему
    for i in range(1, NUM_SEGMENTS):
        dx = segments[i - 1][0] - segments[i][0]
        dy = segments[i - 1][1] - segments[i][1]
        angle = math.atan2(dy, dx)

        # Фиксируем расстояние между звеньями
        segments[i][0] = segments[i - 1][0] - math.cos(angle) * SEG_DISTANCE
        segments[i][1] = segments[i - 1][1] - math.sin(angle) * SEG_DISTANCE


clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Логика: голова следует за мышкой
    mx, my = pygame.mouse.get_pos()
    move_lizard(mx, my)

    # Отрисовка
    rend.draw_color = (30, 40, 30, 255)  # Темный фон
    rend.clear()

    # Рисуем сегменты (от хвоста к голове)
    for i in range(NUM_SEGMENTS - 1, -1, -1):
        # Процедурно меняем размер: голова и пузо толще, хвост тоньше
        size = int(10 + math.sin(i * 0.3 + 2) * 8)

        # Цвет: градиент от зеленого к желтому
        rend.draw_color = (50 + i * 10, 200 - i * 5, 50, 255)

        # В SDL2 Renderer нет круга, рисуем квадратами (или можно текстурой)
        rect = (int(segments[i][0] - size // 2), int(segments[i][1] - size // 2), size, size)
        rend.fill_rect(rect)

    rend.present()
    clock.tick(60)

pygame.quit()
