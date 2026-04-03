import pygame
import math

# Инициализация
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Настройки карточек
cards = [{"id": i, "color": (50 + i * 20 % 200, 100, 200)} for i in range(15)]
scroll = 0.0  # Текущая позиция скролла
target_scroll = 0.0  # Целевая позиция (куда плавно стремимся)

running = True
while running:
    screen.fill((20, 20, 25))  # Темный фон

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Скролл мышью
        if event.type == pygame.MOUSEWHEEL:
            target_scroll -= event.y * 0.4  # Чувствительность скролла

    # Плавное приближение scroll к target_scroll (линейная интерполяция)
    scroll += (target_scroll - scroll) * 0.1

    # Сортируем карточки, чтобы те, что дальше от центра, рисовались первыми (Z-order)
    sorted_cards = sorted(cards, key=lambda c: abs(c['id'] - scroll), reverse=True)

    for card in sorted_cards:
        # Относительная позиция карточки (0 — центр экрана)
        rel_pos = card['id'] - scroll

        # 1. Горизонтальное смещение
        spacing = 150
        x = WIDTH // 2 + rel_pos * spacing

        # 2. Эффект 3D подъема и масштаба
        # influence будет 1.0 в центре и стремиться к 0 при удалении
        dist = abs(rel_pos)
        influence = max(0, 1 - dist * 0.8)

        # Поднимаем центральную карточку вверх
        lift = influence * 120
        # Увеличиваем центральную карточку
        scale = 1.0 + influence * 0.4

        card_w, card_h = 120 * scale, 180 * scale

        # Создаем прямоугольник карточки
        rect = pygame.Rect(0, 0, card_w, card_h)
        rect.center = (x, HEIGHT // 2 + 50 - lift)

        # 3. Визуальные эффекты (затенение)
        shade = max(0.3, influence)  # Чем дальше, тем темнее
        color = [min(255, c * shade) for c in card['color']]

        # Рисуем тень (опционально)
        shadow_rect = rect.copy()
        shadow_rect.move_ip(5, 5)
        pygame.draw.rect(screen, (10, 10, 10), shadow_rect, border_radius=12)

        # Рисуем саму карточку
        pygame.draw.rect(screen, color, rect, border_radius=12)
        # Белая рамка
        pygame.draw.rect(screen, (200, 200, 200), rect, 2, border_radius=12)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
