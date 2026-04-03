import pygame


class SnaringCursor:
    def __init__(self):
        self.pos = pygame.Vector2(0, 0)
        self.target_size = pygame.Vector2(30, 30)
        self.current_size = pygame.Vector2(30, 30)
        self.color = pygame.Color(0, 255, 200)
        self.snared_target = None  # Объект, который мы сейчас "едим"
        self.eat_progress = 0

    def update(self, targets):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        self.pos = mouse_pos

        # Проверяем, наведены ли мы на какой-то прямоугольник
        hovered = None
        for t in targets:
            if t.collidepoint(mouse_pos):
                hovered = t
                break

        if hovered:
            # Обволакиваем: цель по размеру чуть больше объекта
            self.target_size = pygame.Vector2(hovered.width + 15, hovered.height + 15)
            self.color = self.color.lerp((255, 255, 255), 0.1)  # Белеет при поглощении
            self.eat_progress += 1

            # Если "ели" достаточно долго (например, 1 секунду при 60 FPS)
            if self.eat_progress > 60:
                targets.remove(hovered)
                self.eat_progress = 0
        else:
            # Возвращаемся в обычное состояние
            self.target_size = pygame.Vector2(30, 30)
            self.color = self.color.lerp((0, 255, 200), 0.1)
            self.eat_progress = 0

        # Плавное изменение размера (Lerp)
        self.current_size += (self.target_size - self.current_size) * 0.15

    def draw(self, surface):
        # Рисуем полупрозрачную "оболочку"
        rect_surf = pygame.Surface((self.current_size.x, self.current_size.y), pygame.SRCALPHA)
        # Рисуем рамку и заливку
        alpha = 100 + (self.eat_progress * 2)  # Становится ярче при поедании
        pygame.draw.rect(rect_surf, (*self.color[:3], alpha), rect_surf.get_rect(), border_radius=10)
        pygame.draw.rect(rect_surf, self.color, rect_surf.get_rect(), width=2, border_radius=10)

        rect = rect_surf.get_rect(center=self.pos)
        surface.blit(rect_surf, rect.topleft)


# --- Инициализация ---
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.mouse.set_visible(False)
clock = pygame.tick.Clock() if hasattr(pygame, 'tick') else pygame.time.Clock()

cursor = SnaringCursor()
food_rects = [pygame.Rect(200, 250, 80, 60), pygame.Rect(500, 150, 100, 100)]

running = True
while running:
    screen.fill((15, 15, 25))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Рисуем еду
    for r in food_rects:
        pygame.draw.rect(screen, (70, 70, 90), r, border_radius=5)

    # Логика и отрисовка курсора
    cursor.update(food_rects)
    cursor.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
