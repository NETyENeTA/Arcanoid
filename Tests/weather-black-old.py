import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Эффект погоды - Снег")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (50, 50, 50)
GRAY = (100, 100, 100)


# Класс для частиц снега
class SnowFlake:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-HEIGHT, 0)
        self.size = random.randint(2, 5)
        self.speed = random.uniform(1, 3)
        self.swing = random.uniform(0.5, 2)  # амплитуда покачивания
        self.offset = random.uniform(0, 100)  # смещение для синусоиды

    def fall(self):
        # Движение вниз с покачиванием
        self.y += self.speed
        self.x += math.sin((self.y + self.offset) * 0.02) * self.swing * 0.5

        # Сброс вверх, если упал за экран
        if self.y > HEIGHT:
            self.y = random.randint(-50, -10)
            self.x = random.randint(0, WIDTH)
            self.speed = random.uniform(1, 3)
            self.size = random.randint(2, 5)

    def draw(self, surface):
        # Рисуем частицу (темно-серый круг)
        pygame.draw.circle(surface, DARK_GRAY, (int(self.x), int(self.y)), self.size)

        # Добавляем немного вариации цвета
        if self.size > 3:
            pygame.draw.circle(surface, GRAY, (int(self.x - 1), int(self.y - 1)), self.size - 1)


# Версия для дождя (раскомментируйте и используйте вместо SnowFlake)
class RainDrop:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-HEIGHT, 0)
        self.length = random.randint(10, 20)
        self.speed = random.uniform(5, 10)
        self.thickness = random.randint(1, 2)

    def fall(self):
        self.y += self.speed

        # Сброс вверх, если упал за экран
        if self.y > HEIGHT + self.length:
            self.y = random.randint(-HEIGHT, -10)
            self.x = random.randint(0, WIDTH)
            self.speed = random.uniform(5, 10)

    def draw(self, surface):
        # Рисуем каплю дождя (темно-серая линия)
        end_y = self.y + self.length
        pygame.draw.line(surface, DARK_GRAY,
                         (self.x, self.y),
                         (self.x, end_y),
                         self.thickness)


# Основная функция
def main():
    clock = pygame.time.Clock()

    # Создаем частицы
    particles = []
    num_particles = 300  # количество частиц

    for _ in range(num_particles):
        # particles.append(SnowFlake())  # для снега
        particles.append(RainDrop())  # для дождя

    running = True

    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Очистка экрана (белый фон)
        screen.fill(WHITE)

        # Обновление и отрисовка частиц
        for particle in particles:
            particle.fall()
            particle.draw(screen)

        # Обновление экрана
        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    import math  # для синуса в снеге

    main()