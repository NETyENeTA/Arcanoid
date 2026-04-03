import pygame
import random

# Инициализация
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60
PADDLE_W, PADDLE_H = 120, 15
BALL_RADIUS = 10
BLOCK_W, BLOCK_H = 75, 25
SHADOW_OFFSET = 5  # Смещение тени

# Цвета
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
SHADOW_COLOR = (0, 0, 0, 100)  # RGBA для прозрачности
COLORS = [(255, 80, 80), (80, 255, 80), (80, 80, 255), (255, 255, 80)]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arcanoid with Shadows")
clock = pygame.time.Clock()


# Классы объектов
class GameObject:
    def __init__(self, x, y, w, h, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color

    def draw(self, surface):
        # Рисуем тень (смещаем rect)
        shadow_rect = self.rect.copy()
        shadow_rect.x += SHADOW_OFFSET
        shadow_rect.y += SHADOW_OFFSET

        # Для теней используем отдельную поверхность с поддержкой прозрачности
        shadow_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        shadow_surf.fill(SHADOW_COLOR)
        surface.blit(shadow_surf, shadow_rect)

        # Рисуем основной объект
        pygame.draw.rect(surface, self.color, self.rect, border_radius=5)


# Настройка игры
paddle = GameObject(WIDTH // 2 - PADDLE_W // 2, HEIGHT - 40, PADDLE_W, PADDLE_H, WHITE)
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed = [5 * random.choice([-1, 1]), -5]

# Создание блоков
blocks = []
for row in range(5):
    for col in range(10):
        bx = col * (BLOCK_W + 5) + 5
        margin = (WIDTH - (10 * (BLOCK_W + 5))) // 2
        blocks.append(
            GameObject(margin + col * (BLOCK_W + 5), 50 + row * (BLOCK_H + 5), BLOCK_W, BLOCK_H, random.choice(COLORS)))


def draw_ball_with_shadow(surface, ball_rect):
    # Тень мяча
    pygame.draw.circle(surface, (0, 0, 0, 80), (ball_rect.centerx + 4, ball_rect.centery + 4), BALL_RADIUS)
    # Сам мяч
    pygame.draw.circle(surface, WHITE, ball_rect.center, BALL_RADIUS)


# Игровой цикл
run = True
while run:
    screen.fill((40, 40, 40))  # Темно-серый фон

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Управление платформой
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.rect.left > 0:
        paddle.rect.x -= 8
    if keys[pygame.K_RIGHT] and paddle.rect.right < WIDTH:
        paddle.rect.x += 8

    # Движение мяча
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Коллизии со стенами
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed[0] *= -1
    if ball.top <= 0:
        ball_speed[1] *= -1
    if ball.bottom >= HEIGHT:
        # Рестарт при падении
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_speed[1] = -5

    # Коллизия с платформой
    if ball.colliderect(paddle.rect):
        ball_speed[1] *= -1

    # Коллизии с блоками
    hit_index = ball.collidelist([b.rect for b in blocks])
    if hit_index != -1:
        hit_block = blocks.pop(hit_index)
        ball_speed[1] *= -1

    # Отрисовка
    paddle.draw(screen)
    for block in blocks:
        block.draw(screen)
    draw_ball_with_shadow(screen, ball)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
