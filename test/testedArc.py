import pygame
import random
from pygame._sdl2 import Renderer, Window

# Инициализация
pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

# Цвета
BLACK = (20, 20, 25)
WHITE = (255, 255, 255)
PADDLE_COLOR = (50, 150, 255)
GUN_COLOR = (255, 50, 50)
BONUS_COLOR = (255, 255, 0)

# Создание окна и рендерера SDL2
win = Window("SDL2 Arkanoid", size=(WIDTH, HEIGHT))
renderer = Renderer(win)


class Particle:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.life = 255
        self.color = color

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 15
        return self.life > 0

    def draw(self, ren):
        ren.draw_color = (*self.color, self.life)
        ren.fill_rect(pygame.Rect(int(self.x), int(self.y), 4, 4))


class Bonus:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 15, 15)
        self.speed = 4

    def update(self):
        self.rect.y += self.speed
        return self.rect.y < HEIGHT


class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 4, 12)
        self.speed = -8

    def update(self):
        self.rect.y += self.speed
        return self.rect.y > 0


class Brick:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 75, 25)
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.alive = True
        self.breaking = False
        self.scale = 1.0

    def update(self):
        if self.breaking:
            self.scale -= 0.1
            if self.scale <= 0:
                self.breaking = False
                return False
        return True

    def draw(self, ren):
        if self.alive or self.breaking:
            w = int(self.rect.w * self.scale)
            h = int(self.rect.h * self.scale)
            cx, cy = self.rect.center
            draw_rect = pygame.Rect(cx - w // 2, cy - h // 2, w, h)
            ren.draw_color = self.color
            ren.fill_rect(draw_rect)


# Игровые объекты
paddle = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 40, 100, 15)
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, 12, 12)
ball_speed = [5, -5]

bricks = [Brick(col * 80 + 40, row * 30 + 50) for row in range(5) for col in range(9)]
particles = []
bonuses = []
bullets = []
gun_timer = 0

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0: paddle.x -= 8
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH: paddle.x += 8

    # Логика пушки
    if gun_timer > 0:
        gun_timer -= 1
        if gun_timer % 15 == 0:  # Темп стрельбы
            bullets.append(Bullet(paddle.left + 5, paddle.top))
            bullets.append(Bullet(paddle.right - 10, paddle.top))

    # Движение мяча
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    if ball.left <= 0 or ball.right >= WIDTH: ball_speed[0] *= -1
    if ball.top <= 0: ball_speed[1] *= -1
    if ball.colliderect(paddle): ball_speed[1] = -abs(ball_speed[1])
    if ball.bottom >= HEIGHT:  # Проигрыш - сброс
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_speed = [5, -5]
        gun_timer = 0

    # Обработка блоков
    for brick in bricks:
        if brick.alive:
            # Столкновение с мячом
            if ball.colliderect(brick.rect):
                brick.alive = False
                brick.breaking = True
                ball_speed[1] *= -1
                for _ in range(12): particles.append(Particle(*brick.rect.center, brick.color))
                if random.random() < 0.2: bonuses.append(Bonus(*brick.rect.center))

            # Столкновение с пулями
            for b in bullets[:]:
                if b.rect.colliderect(brick.rect):
                    brick.alive = False
                    brick.breaking = True
                    bullets.remove(b)
                    for _ in range(8): particles.append(Particle(*brick.rect.center, brick.color))

    # Обновление списков
    particles = [p for p in particles if p.update()]
    bullets = [b for b in bullets if b.update()]
    bonuses = [b for b in bonuses if b.update()]
    for b in bonuses[:]:
        if b.rect.colliderect(paddle):
            gun_timer = 300  # 5 секунд стрельбы
            bonuses.remove(b)

    bricks = [b for b in bricks if b.update()]

    # Отрисовка SDL2
    renderer.draw_color = BLACK
    renderer.clear()

    # Рисуем блоки
    for brick in bricks: brick.draw(renderer)

    # Рисуем бонусы и пули
    renderer.draw_color = BONUS_COLOR
    for b in bonuses: renderer.fill_rect(b.rect)
    renderer.draw_color = WHITE
    for b in bullets: renderer.fill_rect(b.rect)

    # Рисуем частицы
    for p in particles: p.draw(renderer)

    # Мяч и платформа
    renderer.draw_color = WHITE
    renderer.fill_rect(ball)
    renderer.draw_color = GUN_COLOR if gun_timer > 0 else PADDLE_COLOR
    renderer.fill_rect(paddle)

    renderer.present()
    clock.tick(FPS)

pygame.quit()
