import pygame


class MagneticCursor1:
    def __init__(self):
        self.visual_pos = pygame.Vector2(0, 0)
        self.current_size = pygame.Vector2(30, 30)
        self.color = pygame.Vector3(0, 255, 200)  # Используем Vector2/3 для плавного перехода цвета

    def update(self, targets):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())

        # По умолчанию цель — мышь и стандартный размер
        target_pos = mouse_pos
        target_size = pygame.Vector2(40, 40)
        target_color = pygame.Vector3(0, 255, 200)

        # Проверяем наведение
        hovered = None
        for t in targets:
            if t.collidepoint(mouse_pos):
                hovered = t
                break

        if hovered:
            # Если навели: цель смещается в центр объекта, размер подстраивается
            target_pos = pygame.Vector2(hovered.center)
            target_size = pygame.Vector2(hovered.width + 20, hovered.height + 20)
            target_color = pygame.Vector3(255, 255, 255)  # Белеет при "захвате"

        # Плавное движение (Lerp) — 0.15 это скорость доводки (0.1 - медленно, 0.5 - быстро)
        self.visual_pos += (target_pos - self.visual_pos) * 0.15
        self.current_size += (target_size - self.current_size) * 0.15

        # Плавная смена цвета
        curr_col_vec = pygame.Vector3(self.color.x, self.color.y, 150)  # Вспомогательный вектор
        curr_col_vec += (target_color - curr_col_vec) * 0.1
        self.color = curr_col_vec

    def draw(self, surface):
        # Создаем поверхность для курсора с прозрачностью
        s = pygame.Surface((int(self.current_size.x), int(self.current_size.y)), pygame.SRCALPHA)

        # Рисуем "обволакивающую" рамку
        rect_color = (int(self.color.x), int(self.color.y), int(self.color.z))

        # Основная полупрозрачная заливка
        pygame.draw.rect(s, (*rect_color, 60), s.get_rect(), border_radius=12)
        # Яркий контур
        pygame.draw.rect(s, rect_color, s.get_rect(), width=3, border_radius=12)

        # Отрисовка по визуальной позиции (центр к центру)
        rect = s.get_rect(center=(int(self.visual_pos.x), int(self.visual_pos.y)))
        surface.blit(s, rect.topleft)


import pygame


class MagneticCursor:
    def __init__(self):
        self.visual_pos = pygame.Vector2(0, 0)
        self.current_size = pygame.Vector2(30, 30)
        self.color = pygame.Vector3(0, 255, 200)
        self.is_hovered = False  # Флаг для отслеживания наведения

    def update(self, targets):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())

        target_pos = mouse_pos
        target_size = pygame.Vector2(10, 10)
        target_color = pygame.Vector3(0, 255, 200)

        hovered = None
        for t in targets:
            if t.collidepoint(mouse_pos):
                hovered = t
                break

        if hovered:
            self.is_hovered = True
            target_pos = pygame.Vector2(hovered.center)
            target_size = pygame.Vector2(hovered.width + 20, hovered.height + 20)
            target_color = pygame.Vector3(255, 255, 255)
        else:
            self.is_hovered = False

        self.visual_pos += (target_pos - self.visual_pos) * 0.15
        self.current_size += (target_size - self.current_size) * 0.15

        curr_col_vec = pygame.Vector3(self.color.x, self.color.y, self.color.z)
        curr_col_vec += (target_color - curr_col_vec) * 0.1
        self.color = curr_col_vec

    def draw(self, surface):
        # 1. Рисуем "магнитную" рамку
        s = pygame.Surface((int(self.current_size.x), int(self.current_size.y)), pygame.SRCALPHA)
        rect_color = (int(self.color.x), int(self.color.y), int(self.color.z))

        radius = 12 if self.is_hovered else 3

        pygame.draw.rect(s, (*rect_color, 60), s.get_rect(), border_radius=12)
        pygame.draw.rect(s, rect_color, s.get_rect(), width=3, border_radius=radius)

        rect = s.get_rect(center=(int(self.visual_pos.x), int(self.visual_pos.y)))
        surface.blit(s, rect.topleft)

        # 2. Рисуем точку, если курсор наведен на объект
        if self.is_hovered:
            # Точка рисуется четко в позиции мыши, а не в визуальной позиции рамки
            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.circle(surface, rect_color, mouse_pos, 4)


# --- Инициализация ---
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

cursor = MagneticCursor()
# Наши объекты
# rects = [pygame.Rect(150, 200, 100, 100), pygame.Rect(500, 350, 150, 80)]
rects = [pygame.Rect((30 + x * 130, 30 + y * 80), (100, 50)) for y in range(3) for x in range(3)]


running = True
while running:
    screen.fill((10, 10, 15))  # Глубокий темный фон

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Рисуем статические объекты
    for r in rects:
        pygame.draw.rect(screen, (40, 45, 60), r, border_radius=10)
        pygame.draw.rect(screen, (60, 65, 80), r, width=1, border_radius=10)

    # Обновляем и рисуем курсор
    cursor.update(rects)
    cursor.draw(screen)

    pygame.display.flip()
    clock.tick(165)

pygame.quit()
