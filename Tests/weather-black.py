import pygame
import random
import sys
import math

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Weather Effect - Snow/Wind")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (50, 50, 50)
GRAY = (100, 100, 100)
LIGHT_GRAY = (150, 150, 150)
RED = (200, 50, 50)
BLUE = (50, 50, 200)


# Класс для частиц снега
class SnowFlake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-HEIGHT, 0)
        self.size = random.randint(2, 6)
        self.speed_y = random.uniform(1, 4)
        self.speed_x = random.uniform(-0.5, 0.5)
        self.wind_effect = random.uniform(0.5, 1.5)
        self.swing_amplitude = random.uniform(0.5, 2)
        self.swing_offset = random.uniform(0, 100)

    def fall(self, wind_speed, wind_direction):
        wind_force = wind_speed * wind_direction * self.wind_effect
        natural_swing = math.sin((self.y + self.swing_offset) * 0.02) * self.swing_amplitude * 0.3

        self.x += wind_force + natural_swing + self.speed_x
        self.y += self.speed_y

        if self.y > HEIGHT + 50 or self.x < -50 or self.x > WIDTH + 50:
            self.reset()
            self.x = random.randint(0, WIDTH)

    def draw(self, surface):
        pygame.draw.circle(surface, DARK_GRAY, (int(self.x), int(self.y)), self.size)
        if self.size > 3:
            pygame.draw.circle(surface, GRAY, (int(self.x - 1), int(self.y - 1)), self.size - 1)


# Класс для частиц дождя
class RainDrop:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-HEIGHT, 0)
        self.length = random.randint(10, 25)
        self.speed_y = random.uniform(8, 15)
        self.speed_x = random.uniform(-1, 1)
        self.wind_effect = random.uniform(0.8, 1.8)
        self.thickness = random.randint(1, 2)

    def fall(self, wind_speed, wind_direction):
        wind_force = wind_speed * wind_direction * self.wind_effect
        self.x += wind_force + self.speed_x
        self.y += self.speed_y
        self.angle = wind_force * 0.1

        if self.y > HEIGHT + self.length or self.x < -50 or self.x > WIDTH + 50:
            self.reset()

    def draw(self, surface):
        end_y = self.y + self.length
        end_x = self.x + self.angle * self.length
        pygame.draw.line(surface, DARK_GRAY,
                         (int(self.x), int(self.y)),
                         (int(end_x), int(end_y)),
                         self.thickness)


# Улучшенный индикатор ветра на английском
class WindIndicator:
    def __init__(self):
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)

        # Цвета для разных режимов
        self.colors = {
            'calm': LIGHT_GRAY,
            'light': GRAY,
            'strong': DARK_GRAY,
            'extreme': BLACK
        }

    def get_wind_description(self, speed):
        if speed < 0.5:
            return "CALM", self.colors['calm']
        elif speed < 3:
            return "LIGHT BREEZE", self.colors['light']
        elif speed < 6:
            return "MODERATE WIND", self.colors['strong']
        else:
            return "STRONG WIND", self.colors['extreme']

    def draw_compass(self, surface, x, y, wind_direction):
        # Рисуем простой компас
        radius = 40
        center = (x, y)

        # Внешний круг
        pygame.draw.circle(surface, LIGHT_GRAY, center, radius, 2)

        # Направления
        directions = ['N', 'E', 'S', 'W']
        angles = [270, 0, 90, 180]  # градусы

        for i, (dir_text, angle) in enumerate(zip(directions, angles)):
            rad = math.radians(angle)
            text_x = x + (radius + 15) * math.cos(rad)
            text_y = y + (radius + 15) * math.sin(rad)
            text = self.font_small.render(dir_text, True, GRAY)
            text_rect = text.get_rect(center=(text_x, text_y))
            surface.blit(text, text_rect)

        # Стрелка ветра
        arrow_length = radius - 5
        if wind_direction > 0:  # ветер на восток
            angle = 0
            color = BLUE
        else:  # ветер на запад
            angle = 180
            color = RED

        rad = math.radians(angle)
        end_x = x + arrow_length * math.cos(rad)
        end_y = y + arrow_length * math.sin(rad)

        # Линия стрелки
        pygame.draw.line(surface, color, center, (end_x, end_y), 3)

        # Наконечник стрелки
        arrow_size = 10
        if wind_direction > 0:
            points = [
                (end_x, end_y),
                (end_x - arrow_size, end_y - arrow_size // 2),
                (end_x - arrow_size, end_y + arrow_size // 2)
            ]
        else:
            points = [
                (end_x, end_y),
                (end_x + arrow_size, end_y - arrow_size // 2),
                (end_x + arrow_size, end_y + arrow_size // 2)
            ]
        pygame.draw.polygon(surface, color, points)

    def draw(self, surface, wind_speed, wind_direction, is_snow):
        # Получаем описание ветра
        description, desc_color = self.get_wind_description(wind_speed)

        # Определяем направление текстом
        if abs(wind_speed) < 0.5:
            direction_symbol = "●"
            direction_text = "No wind"
        elif wind_direction > 0:
            direction_symbol = "→"
            direction_text = "EAST"
        else:
            direction_symbol = "←"
            direction_text = "WEST"

        # Формируем строку скорости
        speed_text = f"{wind_speed:.1f} m/s"

        # Тип осадков
        weather_type = "❄️ SNOW" if is_snow else "💧 RAIN"

        # Верхняя панель
        pygame.draw.rect(surface, WHITE, (0, 0, WIDTH, 100))
        pygame.draw.line(surface, LIGHT_GRAY, (0, 100), (WIDTH, 100), 2)

        # Отображаем информацию
        # Скорость ветра большими цифрами
        speed_display = self.font_large.render(speed_text, True, desc_color)
        surface.blit(speed_display, (20, 20))

        # Направление символом
        dir_display = self.font_large.render(direction_symbol, True, desc_color)
        surface.blit(dir_display, (200, 20))

        # Текстовое направление
        dir_text = self.font_medium.render(direction_text, True, desc_color)
        surface.blit(dir_text, (280, 30))

        # Тип погоды
        weather_display = self.font_medium.render(weather_type, True, DARK_GRAY)
        surface.blit(weather_display, (20, 60))

        # Описание ветра
        desc_display = self.font_small.render(description, True, desc_color)
        surface.blit(desc_display, (200, 65))

        # Компас
        self.draw_compass(surface, 650, 50, wind_direction)

        # Подсказки
        hints = [
            "→ : Wind right",
            "← : Wind left",
            "↓ : Decrease wind",
            "R : Rain mode",
            "S : Snow mode",
            "ESC : Exit"
        ]

        y_offset = HEIGHT - 120
        for i, hint in enumerate(hints):
            hint_surface = self.font_small.render(hint, True, GRAY)
            surface.blit(hint_surface, (WIDTH - 200, y_offset + i * 22))

        # Визуализация силы ветра
        if wind_speed > 0:
            bar_width = 300
            bar_height = 20
            bar_x = 20
            bar_y = HEIGHT - 50

            # Фон бара
            pygame.draw.rect(surface, LIGHT_GRAY, (bar_x, bar_y, bar_width, bar_height), 2)

            # Заполнение в зависимости от силы ветра
            fill_width = int((wind_speed / 8.0) * bar_width)
            fill_color = BLUE if wind_direction > 0 else RED

            if fill_width > 0:
                pygame.draw.rect(surface, fill_color, (bar_x, bar_y, fill_width, bar_height))

            # Метки силы
            for i in range(0, 9, 2):
                mark_x = bar_x + (i / 8.0) * bar_width
                mark_text = self.font_small.render(str(i), True, GRAY)
                surface.blit(mark_text, (mark_x - 5, bar_y - 20))


# Основная функция
def main():
    clock = pygame.time.Clock()

    # Параметры ветра
    wind_speed = 2.0
    wind_direction = 1
    wind_max = 8.0
    wind_min = 0.0

    # Тип осадков
    is_snow = True

    # Создаем частицы
    particles = []
    num_particles = 400

    for _ in range(num_particles):
        if is_snow:
            particles.append(SnowFlake())
        else:
            particles.append(RainDrop())

    # Индикатор ветра
    wind_indicator = WindIndicator()

    running = True

    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # Управление ветром
                elif event.key == pygame.K_RIGHT:
                    wind_direction = 1
                    wind_speed = min(wind_speed + 0.5, wind_max)
                elif event.key == pygame.K_LEFT:
                    wind_direction = -1
                    wind_speed = min(wind_speed + 0.5, wind_max)
                elif event.key == pygame.K_DOWN:
                    wind_speed = max(wind_speed - 0.5, wind_min)
                elif event.key == pygame.K_r:
                    # Переключение на дождь
                    if is_snow:
                        is_snow = False
                        particles = [RainDrop() for _ in range(num_particles)]
                elif event.key == pygame.K_s:
                    # Переключение на снег
                    if not is_snow:
                        is_snow = True
                        particles = [SnowFlake() for _ in range(num_particles)]

        # Очистка экрана (белый фон)
        screen.fill(WHITE)

        # Обновление и отрисовка частиц
        for particle in particles:
            particle.fall(wind_speed, wind_direction)
            particle.draw(screen)

        # Рисуем индикатор ветра
        wind_indicator.draw(screen, wind_speed, wind_direction, is_snow)

        # Обновление экрана
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()