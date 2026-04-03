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
    rotation_angle += 0.1
    scale_factor = math.sin(rotation_angle)  # Значение от -1 до 1

    rotation_angle += 0.1
    scale_factor = math.sin(rotation_angle)  # Значение от -1 до 1

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

    for bonus in bonuses[:]:
        bonus['rect'].y += BONUS_FALL_SPEED

        # Определяем цвет
        b_color = GREEN if bonus['type'] == 'wide' else YELLOW

        # Эффект вращения: создаем поверхность и сжимаем её по ширине
        temp_surf = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.rect(temp_surf, b_color, (0, 0, 25, 25), border_radius=5)

        # Масштабируем ширину (имитация поворота по Y)
        new_w = max(1, int(abs(scale_factor) * 25))
        rotated_surf = pygame.transform.scale(temp_surf, (new_w, 25))

        # Центрируем сжатую картинку на месте бонуса
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
