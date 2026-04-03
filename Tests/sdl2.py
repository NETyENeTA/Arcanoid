import pygame
from pygame._sdl2 import Window, Renderer, Texture
import random

# Инициализация
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 1200, 800
win = Window("GPU Shadow Test", size=(WIDTH, HEIGHT))
renderer = Renderer(win)
renderer.draw_color = (30, 30, 30, 255)  # Цвет фона


class Light:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.color = pygame.Color(
            random.randint(150, 255),
            random.randint(150, 255),
            random.randint(150, 255)
        )


class ShadowCaster:
    def __init__(self, x, y, renderer):
        self.pos = pygame.Vector2(x, y)
        self.size = (50, 50)
        self.center = self.pos + pygame.Vector2(25, 25)

        # 1. Создаем маску один раз на Surface
        surf = pygame.Surface(self.size, pygame.SRCALPHA)
        # Рисуем белый круг (наша форма тени)
        pygame.draw.circle(surf, (255, 255, 255), (25, 25), 25)

        # 2. Конвертируем в Текстуру (в видеопамять GPU)
        self.texture = Texture.from_surface(renderer, surf)
        # 1 — это константа для BLENDMODE_BLEND (альфа-смешивание)
        self.texture.blend_mode = 1

    def draw_shadows(self, lights, renderer):
        for light in lights:
            direction = self.center - light.pos
            dist = direction.magnitude()

            if 0 < dist < 600:
                # Математика тени
                alpha = max(0, min(150, 180 - int(dist * 0.3)))
                offset_val = min(dist * 0.4, 80)
                offset = direction.normalize() * offset_val

                # GPU Магия: мгновенная перекраска без создания новых объектов
                dark = 0.4
                self.texture.color = (
                    int(light.color.r * dark),
                    int(light.color.g * dark),
                    int(light.color.b * dark)
                )
                self.texture.alpha = alpha

                # Отрисовка: передаем строго pygame.Rect
                dest_rect = pygame.Rect(
                    int(self.pos.x + offset.x),
                    int(self.pos.y + offset.y),
                    self.size[0],
                    self.size[1]
                )
                renderer.blit(self.texture, dest_rect)


# Создаем объекты
lights = [Light(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(5)]
# Создаем 200 объектов для серьезного теста
casters = [ShadowCaster(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), renderer) for _ in range(200)]

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            # Первый источник света привязан к мышке
            lights[0].pos = pygame.Vector2(event.pos)

    # Очистка экрана (черный фон)
    renderer.draw_color = (20, 20, 20, 255)
    renderer.clear()

    # 1. Рисуем тени всех объектов
    for caster in casters:
        caster.draw_shadows(lights, renderer)

    # 2. Рисуем сами объекты поверх теней
    renderer.draw_color = (200, 200, 200, 255)
    for caster in casters:
        # Рисуем прямоугольник (тоже через Rect)
        r = pygame.Rect(int(caster.pos.x), int(caster.pos.y), 50, 50)
        renderer.fill_rect(r)

    # Вывод кадра
    renderer.present()

    clock.tick()
    # Обновляем FPS в заголовке
    win.title = f"GPU FPS: {int(clock.get_fps())} | Casters: {len(casters)} | Lights: {len(lights)}"

pygame.quit()
