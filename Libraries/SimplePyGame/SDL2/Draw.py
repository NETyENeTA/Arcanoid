from pygame import Rect
from pygame.time import get_ticks

from Libraries.SimplePyGame.Color import Color
from Libraries.SimplePyGame.Colors import Colors


def draw_horizontal_line(render, x1, x2, y, thickness: int = 1, color: Color | tuple = Colors.BLACK):
    # Устанавливаем цвет
    render.draw_color = color.full if isinstance(color, Color) else color

    # Находим начало и длину
    start_x = min(x1, x2)
    width = abs(x1 - x2)

    # Центрируем по вертикали: смещаем Y вверх на половину толщины
    # Чтобы линия рисовалась ровно ПОСЕРЕДИНЕ координаты y
    rect_y = y - (thickness // 2)

    # Рисуем закрашенный прямоугольник
    render.fill_rect(Rect(start_x, rect_y, width, thickness))


def draw_line(render, start_pos, end_pos, thickness: int = 1, color: Color | tuple | list = Colors.BLACK):
    """
    Рисует толстую вертикальную или горизонтальную линию.
    """
    render.draw_color = color.full if isinstance(color, Color) else color

    x1, y1 = start_pos
    x2, y2 = end_pos

    # Вычисляем размеры прямоугольника
    width = abs(x2 - x1)
    height = abs(y2 - y1)

    # Если это вертикальная линия, ширина будет 0, ставим её равной thickness
    if width == 0:
        width = thickness
        # Центрируем линию, чтобы она шла ровно по координате
        x1 -= thickness // 2
        # Если горизонтальная — высота 0, ставим thickness
    if height == 0:
        height = thickness
        y1 -= thickness // 2

    render.fill_rect(Rect(x1, y1, width, height))


def draw_dashed_line(renderer, rect, color=(255, 255, 255), dash_len=10, gap_len=5, width=3):
    renderer.draw_color = color

    # Скорректируем стороны, чтобы углы не накладывались некрасиво
    # Верх и Низ
    for x in range(rect.left, rect.right, dash_len + gap_len):
        w = min(dash_len, rect.right - x)
        renderer.fill_rect(Rect(x, rect.top - width // 2, w, width))
        renderer.fill_rect(Rect(x, rect.bottom - width // 2, w, width))

    # Лево и Право
    for y in range(rect.top, rect.bottom, dash_len + gap_len):
        h = min(dash_len, rect.bottom - y)
        renderer.fill_rect(Rect(rect.left - width // 2, y, width, h))
        renderer.fill_rect(Rect(rect.right - width // 2, y, width, h))


import pygame as pg


def draw_circular_dashed_rect(renderer, rect, color=(0, 255, 0),
                              dash_len=10, gap_len=10, width=2, speed=60):
    renderer.draw_color = color

    # 1. Считаем параметры периметра
    w, h = rect.width, rect.height
    perimeter = 2 * (w + h)
    step = dash_len + gap_len

    # 2. Смещение на основе времени для эффекта бега
    offset = (pg.time.get_ticks() * speed / 1000) % step

    # 3. Идем по всему периметру с шагом step
    # distance — это расстояние от верхнего левого угла (0,0) по часовой стрелке
    for d in range(int(-offset), int(perimeter), step):
        # Рисуем только штрих (dash_len)
        for i in range(dash_len):
            curr_d = (d + i) % perimeter  # Текущая точка на периметре

            # Определяем координаты (x, y) на основе дистанции curr_d
            if curr_d < w:  # Верхняя грань
                x, y = rect.left + curr_d, rect.top
            elif curr_d < w + h:  # Правая грань
                x, y = rect.right, rect.top + (curr_d - w)
            elif curr_d < 2 * w + h:  # Нижняя грань
                x, y = rect.right - (curr_d - (w + h)), rect.bottom
            else:  # Левая грань
                x, y = rect.left, rect.bottom - (curr_d - (2 * w + h))

            # Рисуем точку (маленький квадратик толщиной width)
            # Примечание: для скорости лучше рисовать штрихи целиком,
            # но попиксельно — самый точный способ "поворота" на углах.
            renderer.fill_rect(pg.Rect(x - width // 2, y - width // 2, width, width))


def draw_animated_dashed_rect(renderer, rect, color=(255, 255, 0),
                              dash_len=10, gap_len=10, width=2, speed=30):
    renderer.draw_color = color

    # Считаем общее расстояние (цикл одного штриха и одного пропуска)
    total_step = dash_len + gap_len

    # Вычисляем смещение на основе времени (в пикселях)
    # % total_step зацикливает анимацию, чтобы offset не рос бесконечно
    offset = (get_ticks() * speed / 1000) % total_step

    # 1. Верхняя и нижняя стороны
    for x in range(rect.left - int(offset), rect.right, total_step):
        # Рисуем только ту часть штриха, которая попадает внутрь границ rect
        draw_x = max(x, rect.left)
        w = min(dash_len - (draw_x - x), rect.right - draw_x)
        if w > 0:
            renderer.fill_rect(Rect(draw_x, rect.top - width // 2, w, width))
            renderer.fill_rect(Rect(draw_x, rect.bottom - width // 2, w, width))

    # 2. Левая и правая стороны
    for y in range(rect.top - int(offset), rect.bottom, total_step):
        draw_y = max(y, rect.top)
        h = min(dash_len - (draw_y - y), rect.bottom - draw_y)
        if h > 0:
            renderer.fill_rect(Rect(rect.left - width // 2, draw_y, width, h))
            renderer.fill_rect(Rect(rect.right - width // 2, draw_y, width, h))
