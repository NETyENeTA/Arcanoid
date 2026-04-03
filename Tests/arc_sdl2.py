import pygame
from pygame._sdl2 import Window, Renderer, Texture
import random
import os

# Включаем сглаживание для мягких теней
os.environ['SDL_HINT_RENDER_SCALE_QUALITY'] = '1'

pygame.init()

WIDTH, HEIGHT = 1000, 800
win = Window("GPU Arcanoid + Shadows", size=(WIDTH, HEIGHT))
renderer = Renderer(win)

PADDLE_WIDTH, PADDLE_HEIGHT = 120, 20
BALL_RADIUS = 10
BLOCK_WIDTH, BLOCK_HEIGHT = 70, 25


class Game:
    def __init__(self):
        # 1. Текстура Блока
        surf = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        surf.fill((255, 255, 255))
        pygame.draw.rect(surf, (180, 180, 180), surf.get_rect(), 2)
        self.block_tex = Texture.from_surface(renderer, surf)

        # 2. Текстура МЯЧА (Света)
        ball_surf = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(ball_surf, (255, 255, 255), (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.ball_tex = Texture.from_surface(renderer, ball_surf)

        # 3. Текстура ТЕНИ (Маленькая для блюра)
        # Рисуем маску 20x20, которую GPU растянет в мягкую тень
        shadow_surf = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, (255, 255, 255), (0, 0, 20, 20))
        self.shadow_tex = Texture.from_surface(renderer, shadow_surf)
        self.shadow_tex.blend_mode = 1  # Смешивание альфы

        self.paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 60, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ball = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
        self.ball_vel = pygame.Vector2(4, -4)

        self.blocks = []
        for y in range(8):
            for x in range(WIDTH // (BLOCK_WIDTH + 8)):
                r = pygame.Rect(x * (BLOCK_WIDTH + 8) + 20, y * (BLOCK_HEIGHT + 8) + 60, BLOCK_WIDTH, BLOCK_HEIGHT)
                color = (random.randint(80, 200), random.randint(80, 200), random.randint(200, 255))
                self.blocks.append({'rect': r, 'color': color})

    def update(self):
        mx, _ = pygame.mouse.get_pos()
        self.paddle.centerx = mx
        self.ball += self.ball_vel

        if self.ball.x <= 0 or self.ball.x >= WIDTH: self.ball_vel.x *= -1
        if self.ball.y <= 0: self.ball_vel.y *= -1

        ball_rect = pygame.Rect(int(self.ball.x - BALL_RADIUS), int(self.ball.y - BALL_RADIUS), BALL_RADIUS * 2,
                                BALL_RADIUS * 2)

        if ball_rect.colliderect(self.paddle):
            self.ball_vel.y *= -1
            self.ball.y = self.paddle.top - BALL_RADIUS

        for block in self.blocks[:]:
            if ball_rect.colliderect(block['rect']):
                self.ball_vel.y *= -1
                self.blocks.remove(block)
                break

    def draw_shadow(self, target_rect, light_pos, strength=0.5):
        # Расчет вектора тени от мяча
        target_center = pygame.Vector2(target_rect.center)
        dir_vec = target_center - light_pos
        dist = dir_vec.magnitude()

        if dist > 0:
            # Длина тени и прозрачность зависят от расстояния
            offset = dir_vec.normalize() * min(dist * 0.2, 40)
            alpha = max(20, min(100, 150 - int(dist * 0.2)))

            # Настройка текстуры тени
            self.shadow_tex.color = (0, 0, 0)  # Черная тень
            self.shadow_tex.alpha = alpha

            # Смещаем и немного увеличиваем тень для эффекта объема
            shadow_rect = pygame.Rect(
                int(target_rect.x + offset.x),
                int(target_rect.y + offset.y),
                target_rect.width + 4,
                target_rect.height + 4
            )
            renderer.blit(self.shadow_tex, shadow_rect)

    def draw(self):
        renderer.draw_color = (15, 15, 20, 255)  # Темный фон
        renderer.clear()

        # 1. Сначала рисуем ТЕНИ (под объектами)
        for block in self.blocks:
            self.draw_shadow(block['rect'], self.ball)
        self.draw_shadow(self.paddle, self.ball)

        # 2. Рисуем БЛОКИ
        for block in self.blocks:
            self.block_tex.color = block['color']
            renderer.blit(self.block_tex, block['rect'])

        # 3. Рисуем ПЛАТФОРМУ
        renderer.draw_color = (255, 255, 255, 255)
        renderer.fill_rect(self.paddle)

        # 4. Рисуем МЯЧ (наш источник света)
        ball_rect = pygame.Rect(int(self.ball.x - BALL_RADIUS), int(self.ball.y - BALL_RADIUS), BALL_RADIUS * 2,
                                BALL_RADIUS * 2)
        self.ball_tex.color = (255, 255, 0)  # Желтый светящийся мяч
        renderer.blit(self.ball_tex, ball_rect)

        renderer.present()


game = Game()
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit();
            exit()

    game.update()
    game.draw()
    clock.tick(190)
    win.title = f"GPU Shadows | FPS: {int(clock.get_fps())} | Blocks: {len(game.blocks)}"
