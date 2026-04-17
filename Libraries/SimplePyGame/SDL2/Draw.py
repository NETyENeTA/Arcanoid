from pygame import Rect
from pygame.time import get_ticks

from Libraries.SimplePyGame.Color import Color
from Libraries.SimplePyGame.Colors import Colors

from math import sin, cos, pi, atan2


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


def draw_dashed_circle(renderer, center, radius, color=(0, 255, 0),
                       dash_len=10, gap_len=10, width=2, speed=60):
    renderer.draw_color = color

    # 1. Считаем длину окружности
    circumference = 2 * pi * radius
    step_len = dash_len + gap_len  # Полный цикл (штрих + пробел)

    # 2. Смещение для анимации "бега"
    # Переводим время в пиксели смещения, а затем в радианы
    offset_px = (pg.time.get_ticks() * speed / 1000) % step_len
    offset_rad = (offset_px / circumference) * (2 * pi)

    # 3. Рисуем сегментами
    # Количество сегментов (штрихов) на круге
    num_dashes = int(circumference / step_len)

    for i in range(num_dashes + 1):
        # Начальный и конечный угол для каждого штриха (в радианах)
        start_angle = (i * step_len / circumference) * (2 * pi) + offset_rad
        end_angle = start_angle + (dash_len / circumference) * (2 * pi)

        # Рисуем штрих как несколько маленьких отрезков для гладкости
        num_segments = 5  # Чем больше, тем плавнее изгиб штриха
        for j in range(num_segments):
            seg_start = start_angle + (end_angle - start_angle) * (j / num_segments)
            seg_end = start_angle + (end_angle - start_angle) * ((j + 1) / num_segments)

            x1 = center[0] + cos(seg_start) * radius
            y1 = center[1] + sin(seg_start) * radius
            x2 = center[0] + cos(seg_end) * radius
            y2 = center[1] + sin(seg_end) * radius

            # В SDL2 Renderer рисуем линию
            renderer.draw_line((int(x1), int(y1)), (int(x2), int(y2)))

            # Если нужна толщина, можно нарисовать рядом еще линии или fill_rect
            if width > 1:
                renderer.fill_rect(pg.Rect(int(x1) - width // 2, int(y1) - width // 2, width, width))


def draw_animated_line(
    renderer,
    start_pos,
    end_pos,
    color=(255, 255, 0),
    dash_len=10,
    gap_len=5,
    width=3,
    speed=30,
):
    """Рисует анимированную пунктирную линию с использованием вашего renderer.

    :param renderer: Объект рендерера (должен иметь метод fill_rect и свойство
    draw_color).
    :param start_pos: Кортеж (x, y) начала линии.
    :param end_pos: Кортеж (x, y) конца линии.
    """
    # Установка цвета через свойство вашего рендерера
    renderer.draw_color = color

    p1 = pg.math.Vector2(start_pos)
    p2 = pg.math.Vector2(end_pos)

    # Вычисление вектора направления и длины
    direction = p2 - p1
    total_length = direction.length()

    if total_length == 0:
        return

    direction.normalize_ip()

    total_step = dash_len + gap_len
    offset = (pg.time.get_ticks() * speed / 1000) % total_step

    # Вычисляем угол наклона линии для правильного поворота "прямоугольников"
    # Это нужно, чтобы толщина линии (width) корректно ложилась под наклоном
    angle = atan2(direction.y, direction.x)
    cos_a = cos(angle)
    sin_a = sin(angle)

    current_dist = -offset

    while current_dist < total_length:
        dash_start_dist = max(0, current_dist)
        dash_end_dist = min(current_dist + dash_len, total_length)

        if dash_start_dist < dash_end_dist:
            # Длина конкретно этого штриха
            current_dash_len = dash_end_dist - dash_start_dist

            # Находим центр штриха
            mid_dist = dash_start_dist + current_dash_len / 2
            mid_pos = p1 + direction * mid_dist

            # Рисуем штрих через fill_rect.
            # Если линия идет под наклоном, мы аппроксимируем её точками/квадратами.
            # Для идеальной сплошной линии под углом нужен полигон, но для пунктира
            # отрисовка через маленькие повернутые заполнения работает отлично.
            if abs(cos_a) > abs(sin_a):
                # Линия ближе к горизонтальной
                for step in range(int(current_dash_len)):
                    pos = (
                        p1
                        + direction * (dash_start_dist + step)
                        - pg.math.Vector2(0, width // 2)
                    )
                    renderer.fill_rect(
                        pg.Rect(int(pos.x), int(pos.y), 1, width)
                    )
            else:
                # Линия ближе к вертикальной
                for step in range(int(current_dash_len)):
                    pos = (
                        p1
                        + direction * (dash_start_dist + step)
                        - pg.math.Vector2(width // 2, 0)
                    )
                    renderer.fill_rect(
                        pg.Rect(int(pos.x), int(pos.y), width, 1)
                    )

        current_dist += total_step