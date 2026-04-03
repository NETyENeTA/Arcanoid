import pygame
from pygame._sdl2 import Window, Renderer
import math

WIDTH, HEIGHT = 800, 600


def solve_ik(root, target, len1, len2, flip=1):
    """Вычисляет IK. flip=1 сгиб вниз, flip=-1 сгиб вверх."""
    dx, dy = target[0] - root[0], target[1] - root[1]
    dist = math.hypot(dx, dy)
    dist = max(0.1, min(len1 + len2 - 0.1, dist))

    angle_to_target = math.atan2(dy, dx)
    cos_a = (len1 ** 2 + dist ** 2 - len2 ** 2) / (2 * len1 * dist)
    inner_angle = math.acos(max(-1, min(1, cos_a)))

    # Вычисляем локоть с учетом стороны сгиба (flip)
    elbow = (root[0] + math.cos(angle_to_target - inner_angle * flip) * len1,
             root[1] + math.sin(angle_to_target - inner_angle * flip) * len1)

    hand = (root[0] + math.cos(angle_to_target) * dist,
            root[1] + math.sin(angle_to_target) * dist)

    return elbow, hand


def main():
    pygame.init()
    win = Window("SDL2 Full Body IK", size=(WIDTH, HEIGHT))
    rend = Renderer(win)

    clock = pygame.time.Clock()
    L1, L2 = 40, 35
    time_passed = 0.0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False

        mx, my = pygame.mouse.get_pos()
        time_passed += 0.05

        # 1. Параметры тела
        base_x, base_y = WIDTH // 2, HEIGHT // 2 + 50  # Точка таза (статична)
        breath = math.sin(time_passed) * 3

        # 2. Наклон торса (зависит от удаления мыши от центра)
        tilt = (mx - base_x) * 0.15  # Коэффициент наклона
        tilt = max(-30, min(30, tilt))  # Ограничиваем наклон

        # Позиция шеи/плеч (смещается по X от наклона и по Y от дыхания)
        neck_pos = (base_x + tilt, base_y - 100 + breath)

        # 3. Расчет обеих рук
        # Правая рука тянется к мышке
        elbow_r, hand_r = solve_ik(neck_pos, (mx, my), L1, L2)
        # Левая рука тянется к той же цели, но чуть ниже (подхватывает)
        elbow_l, hand_l = solve_ik(neck_pos, (mx, my + 40), L1, L2, flip=-1)

        # Рендеринг
        rend.draw_color = (10, 10, 15, 255)
        rend.clear()
        rend.draw_color = (220, 220, 220, 255)

        # Голова (наклоняется вместе с шеей)
        rend.draw_rect(pygame.Rect(neck_pos[0] - 15, neck_pos[1] - 40, 30, 30))

        # Торс (от таза до шеи)
        rend.draw_line((base_x, base_y), neck_pos)

        # Ноги (от таза к стопам)
        rend.draw_line((base_x, base_y), (base_x - 25, base_y + 80))
        rend.draw_line((base_x, base_y), (base_x + 25, base_y + 80))

        # Отрисовка рук
        rend.draw_color = (0, 255, 200, 255)  # Правая
        rend.draw_line(neck_pos, elbow_r)
        rend.draw_line(elbow_r, hand_r)

        rend.draw_color = (255, 100, 0, 255)  # Левая
        rend.draw_line(neck_pos, elbow_l)
        rend.draw_line(elbow_l, hand_l)

        rend.present()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
