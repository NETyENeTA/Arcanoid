import pygame
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

cards = [{"id": i, "color": (40 + i * 15 % 200, 80, 220)} for i in range(20)]
scroll = 0.0
target_scroll = 0.0

# Коэффициенты наклона диагонали
DIAG_X = 100  # Смещение по горизонтали между картами
DIAG_Y = 40  # Смещение по вертикали (эффект глубины/ряда)

running = True
while running:
    screen.fill((15, 15, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.MOUSEWHEEL:
            target_scroll -= event.y * 0.5

    scroll += (target_scroll - scroll) * 0.1

    # Сортировка: сначала рисуем дальние (те, у кого ID больше или меньше текущего скролла)
    # Чтобы центральная всегда была поверх всех
    sorted_cards = sorted(cards, key=lambda c: abs(c['id'] - scroll), reverse=True)

    for card in sorted_cards:
        rel_pos = card['id'] - scroll

        # 1. Базовая позиция по диагонали
        base_x = WIDTH // 2 + rel_pos * DIAG_X
        base_y = HEIGHT // 2 + rel_pos * DIAG_Y

        # 2. Эффект "вытягивания" (3D подъем)
        # Считаем близость к центру (от 0.0 до 1.0)
        dist = abs(rel_pos)
        influence = max(0, 1 - dist * 0.7)

        # Поднимаем карточку ПЕРПЕНДИКУЛЯРНО линии диагонали (или просто вверх для акцента)
        lift_x = influence * -30  # Немного влево при подъеме
        lift_y = influence * 150  # Сильно вверх

        scale = 1.0 + influence * 0.5

        # Финальные координаты
        x = base_x + lift_x
        y = base_y - lift_y

        # Отрисовка
        card_w, card_h = 130 * scale, 180 * scale
        rect = pygame.Rect(0, 0, card_w, card_h)
        rect.center = (x, y)

        # Затемнение для глубины
        shade = max(0.2, influence)
        color = [min(255, c * shade) for c in card['color']]

        # Тень
        shadow_rect = rect.copy()
        shadow_rect.move_ip(8, 8)
        pygame.draw.rect(screen, (5, 5, 10), shadow_rect, border_radius=15)

        # Карточка
        pygame.draw.rect(screen, color, rect, border_radius=15)
        # Блик на грани (добавляет объема)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2 if influence < 0.8 else 4, border_radius=15)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
