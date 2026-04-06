import pygame
import random
import math

# Инициализация
pygame.init()

# Константы экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arcanoid 3D-Bonuses")
clock = pygame.time.Clock()
FPS = 60

# Цвета
BLACK = (20, 20, 20)
WHITE = (255, 255, 255)
GREEN = (50, 255, 50)
YELLOW = (255, 255, 0)
RED = (255, 50, 50)

# Настройки игрока
paddle_w, paddle_h = 120, 15
paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - 40, paddle_w, paddle_h)
paddle_speed = 10

# Настройки мяча
ball_radius = 8
ball_speed = 5
ball_rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, ball_radius * 2, ball_radius * 2)
dx, dy = ball_speed, -ball_speed

# Сетка кирпичей
blocks = []
block_colors = []
for i in range(10):  # 10 колонок
    for j in range(6):  # 6 рядов
        rect = pygame.Rect(15 + i * 78, 50 + j * 35, 70, 25)
        blocks.append(rect)
        block_colors.append((random.randint(100, 255), random.randint(50, 150), 255))

# Бонусы
bonuses = []  # Список словарей: {'rect': Rect, 'type': str}
BONUS_FALL_SPEED = 3
rotation_angle = 0  # Для эффекта вращения по Y


def spawn_bonus(pos):


    if random.random() < 1:  # 25% шанс выпадения
        b_type = random.choice(['wide', 'fast'])
        bonuses.append({'rect': pygame.Rect(pos[0], pos[1], 25, 25), 'type': b_type})


running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление платформой
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.right += paddle_speed

    # Движение мяча
    ball_rect.x += dx
    ball_rect.y += dy

    # Отскоки от стен
    if ball_rect.left <= 0 or ball_rect.right >= WIDTH:
        dx *= -1
    if ball_rect.top <= 0:
        dy *= -1
    if ball_rect.bottom >= HEIGHT:
        print("Игра окончена!")
        running = False

    # Отскок от платформы
    if ball_rect.colliderect(paddle) and dy > 0:
        dy *= -1

    # Столкновение с кирпичами
    hit_idx = ball_rect.collidelist(blocks)
    if hit_idx != -1:
        hit_rect = blocks.pop(hit_idx)
        block_colors.pop(hit_idx)
        dy *= -1
        spawn_bonus(hit_rect.center)

    # Логика и отрисовка бонусов (Вращение по Y)
    # rotation_angle += 0.1
    # scale_factor = math.sin(rotation_angle)  # Значение от -1 до 1
    #
    # rotation_angle += 0.1
    # scale_factor = math.sin(rotation_angle)  # Значение от -1 до 1

    # # В начале цикла (где расчеты)
    # time_ms = pygame.time.get_ticks()
    # # scale_factor меняется от -1 до 1
    # scale_factor = math.sin(time_ms / 250)
    # # Чем ближе масштаб к 0, тем сильнее "блик" (яркость)
    # flash_intensity = int((1 - abs(scale_factor)) * 150)

    # В начале цикла (где расчеты)
    # time_ms = pygame.time.get_ticks()
    # # scale_factor для ширины (от -1 до 1)
    # scale_raw = math.sin(time_ms / 400)
    # scale_factor = abs(scale_raw)
    #
    # # Интенсивность блика: максимум (180), когда бонус ребром (scale_factor близок к 0)
    # flash_alpha = int((1 - scale_factor) * 180)

    # for bonus in bonuses[:]:
    #     bonus['rect'].y += BONUS_FALL_SPEED
    #
    #     # Выбираем цвет
    #     b_color = GREEN if bonus['type'] == 'wide' else YELLOW
    #
    #     # Создаем базовую поверхность бонуса
    #     temp_surf = pygame.Surface((25, 25), pygame.SRCALPHA)
    #     pygame.draw.rect(temp_surf, b_color, (0, 0, 25, 25), border_radius=5)
    #
    #     # --- ВРАЩЕНИЕ ПО ОСИ Y ---
    #     # Изменяем ВЫСОТУ (второй параметр в scale), оставляя ширину 25
    #     new_h = max(1, int(abs(scale_factor) * 25))
    #     rotated_surf = pygame.transform.scale(temp_surf, (25, new_h))
    #
    #     # Центрируем сжатую по вертикали картинку
    #     rot_rect = rotated_surf.get_rect(center=bonus['rect'].center)
    #     screen.blit(rotated_surf, rot_rect)
    #
    #     # Проверка на поимку платформой
    #     if bonus['rect'].colliderect(paddle):
    #         if bonus['type'] == 'wide':
    #             paddle.width += 40
    #         elif bonus['type'] == 'fast':
    #             dx *= 1.2
    #             dy *= 1.2
    #         bonuses.remove(bonus)
    #     elif bonus['rect'].top > HEIGHT:
    #         bonuses.remove(bonus)

    # В начале цикла (где расчеты)
    time_ms = pygame.time.get_ticks()
    # Обычный sin дает значение от -1 до 1
    raw_sin = math.sin(time_ms / 250)
    scale_factor = abs(raw_sin)  # Ширина всегда положительная

    for bonus in bonuses[:]:
        bonus['rect'].y += BONUS_FALL_SPEED

        # Базовый цвет (зеленый или желтый)
        base_color = GREEN if bonus['type'] == 'wide' else YELLOW

        # --- ЭФФЕКТ ЗАДНЕЙ СТОРОНЫ ---
        if raw_sin > 0:
            # Лицевая сторона: обычный цвет + блик при повороте
            display_color = base_color
            flash_alpha = int((1 - scale_factor) * 150)
        else:
            # Задняя сторона (sin < 0): делаем цвет темнее (умножаем компоненты на 0.6)
            display_color = (int(base_color[0] * 0.6), int(base_color[1] * 0.6), int(base_color[2] * 0.6))
            flash_alpha = 0  # На задней стороне блик обычно не виден

        # 1. Рисуем бонус
        temp_surf = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.rect(temp_surf, display_color, (0, 0, 25, 25), border_radius=5)

        # 2. Накладываем блик (только для лицевой стороны)
        if flash_alpha > 0:
            flash_surf = pygame.Surface((25, 25), pygame.SRCALPHA)
            pygame.draw.rect(flash_surf, (255, 255, 255), (0, 0, 25, 25), border_radius=5)
            flash_surf.set_alpha(flash_alpha)
            temp_surf.blit(flash_surf, (0, 0))

        # 3. Масштабируем ширину
        new_w = max(1, int(scale_factor * 25))
        rotated_surf = pygame.transform.scale(temp_surf, (new_w, 25))

        # 4. Центрируем и рисуем
        rot_rect = rotated_surf.get_rect(center=bonus['rect'].center)
        screen.blit(rotated_surf, rot_rect)

        # Сбор бонуса
        if bonus['rect'].colliderect(paddle):
            if bonus['type'] == 'wide':
                paddle.width += 40
            elif bonus['type'] == 'fast':
                dx *= 1.2
                dy *= 1.2
            bonuses.remove(bonus)
        elif bonus['rect'].top > HEIGHT:
            bonuses.remove(bonus)

    # Отрисовка кирпичей, платформы и мяча
    for i, block in enumerate(blocks):
        pygame.draw.rect(screen, block_colors[i], block, border_radius=3)

    pygame.draw.rect(screen, WHITE, paddle, border_radius=7)
    pygame.draw.circle(screen, RED, ball_rect.center, ball_radius)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
