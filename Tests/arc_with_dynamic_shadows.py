import pygame
import random
from pygame.math import Vector2

pygame.init()

# Настройки
WIDTH, HEIGHT = 800, 600
FPS = 60
BLOCK_W, BLOCK_H = 75, 25
BALL_RADIUS = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


class Entity:
    def __init__(self, x, y, w, h, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.base_color = pygame.Color(color)
        self.current_color = self.base_color
        self.scale = 1.0

    def update(self, light_pos):
        dist = Vector2(self.rect.center).distance_to(Vector2(light_pos))
        # Эффект увеличения и подсветки
        target_scale = 1.2 if dist < 100 else 1.0
        self.scale += (target_scale - self.scale) * 0.1
        self.current_color = self.base_color.lerp((255, 255, 255), 0.4 if dist < 100 else 0)

    def get_draw_rect(self):
        w, h = int(self.rect.width * self.scale), int(self.rect.height * self.scale)
        res = pygame.Rect(0, 0, w, h)
        res.center = self.rect.center
        return res

    def draw_shadow(self, surface, light_pos):
        draw_rect = self.get_draw_rect()
        direction = Vector2(self.rect.center) - Vector2(light_pos)
        dist = direction.length()

        if dist > 0:
            # Тот самый clamp через max/min
            shadow_len = max(2, min(dist * 0.1, 40))
            offset = direction.normalize() * shadow_len
        else:
            offset = Vector2(0, 0)

        shadow_surf = pygame.Surface((draw_rect.w, draw_rect.h), pygame.SRCALPHA)
        shadow_surf.fill((0, 0, 0, 80))  # Прозрачная тень
        surface.blit(shadow_surf, (draw_rect.x + offset.x, draw_rect.y + offset.y))

    def draw_body(self, surface):
        pygame.draw.rect(surface, self.current_color, self.get_draw_rect(), border_radius=4)


# --- Инициализация объектов ---
blocks = [
    Entity(50 + c * 82, 60 + r * 32, BLOCK_W, BLOCK_H, random.choice([(200, 50, 50), (50, 200, 50), (50, 50, 200)]))
    for r in range(5) for c in range(9)]
paddle = Entity(WIDTH // 2 - 60, HEIGHT - 40, 120, 15, (200, 200, 200))
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed = Vector2(5, -5)

run = True
while run:
    screen.fill((40, 40, 45))
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = False

    # Логика
    paddle.rect.centerx = mouse_pos[0]
    paddle.update(mouse_pos)
    ball.x += ball_speed.x
    ball.y += ball_speed.y

    if ball.left <= 0 or ball.right >= WIDTH: ball_speed.x *= -1
    if ball.top <= 0: ball_speed.y *= -1
    if ball.colliderect(paddle.rect): ball_speed.y *= -1

    for b in blocks[:]:
        b.update(mouse_pos)
        if ball.colliderect(b.rect):
            blocks.remove(b)
            ball_speed.y *= -1

    # --- Рендеринг (ПО СЛОЯМ) ---

    # 1 Слой: Все тени
    paddle.draw_shadow(screen, mouse_pos)
    for b in blocks:
        b.draw_shadow(screen, mouse_pos)

    # Тень мяча
    ball_dir = Vector2(ball.center) - Vector2(mouse_pos)
    if ball_dir.length() > 0:
        b_off = ball_dir.normalize() * max(2, min(ball_dir.length() * 0.1, 30))
        pygame.draw.circle(screen, (0, 0, 0, 80), (ball.centerx + b_off.x, ball.centery + b_off.y), BALL_RADIUS)

    # 2 Слой: Все тела объектов
    paddle.draw_body(screen)
    for b in blocks:
        b.draw_body(screen)

    # Мяч (тело)
    pygame.draw.circle(screen, (255, 255, 255), ball.center, BALL_RADIUS)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
