import pygame
from pygame._sdl2 import Window, Renderer, Texture

WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = pygame.Vector2(0, 0.45)

pygame.init()
win = Window("Drag & Jiggle Physics", size=(WIDTH, HEIGHT))
rend = Renderer(win)


def create_circle_texture(renderer, radius, color):
    surf = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
    pygame.draw.ellipse(surf, color, (0, 0, radius * 4, radius * 4))
    return Texture.from_surface(renderer, surf)


skin_color = (255, 185, 185, 255)
circle_tex = create_circle_texture(rend, 50, skin_color)


class JiggleOval:
    def __init__(self, anchor_x, anchor_y, base_w, base_h):
        self.anchor = pygame.Vector2(anchor_x, anchor_y)
        self.pos = pygame.Vector2(anchor_x, anchor_y)
        self.vel = pygame.Vector2(0, 0)
        self.base_w = base_w
        self.base_h = base_h

        self.is_dragging = False
        self.stiffness = 0.5
        self.damping = 0.7
        self.max_dist = 160  # Увеличил, чтобы можно было тянуть дальше

    def update(self):
        if self.is_dragging:
            # Если тянем, позиция стремится к мышке, а скорость гасится
            mx, my = pygame.mouse.get_pos()
            target = pygame.Vector2(mx, my)
            self.vel = (target - self.pos) * 0.3
            self.pos += self.vel
        else:
            # Обычная физика пружины к якорю
            accel = (self.anchor - self.pos) * self.stiffness
            self.vel += accel + GRAVITY
            self.vel *= self.damping
            self.pos += self.vel

        # Ограничитель, чтобы не оторвать совсем
        diff = self.pos - self.anchor
        if diff.length() > self.max_dist:
            self.pos = self.anchor + diff.normalize() * self.max_dist

    def check_click(self, mouse_pos):
        if self.pos.distance_to(mouse_pos) < self.base_w / 2:
            self.is_dragging = True
            return True
        return False

    def draw(self, renderer, texture):
        # Эффект Squash & Stretch от скорости
        stretch_h = self.base_h + (self.vel.y * 1.5)
        stretch_w = self.base_w - abs(self.vel.y * 0.6) + abs(self.vel.x * 0.6)

        draw_w = max(self.base_w * 0.7, min(stretch_w, self.base_w * 1.4))
        draw_h = max(self.base_h * 0.7, min(stretch_h, self.base_h * 1.5))

        dest_rect = pygame.Rect(self.pos.x - draw_w // 2, self.pos.y - draw_h // 2, int(draw_w), int(draw_h))
        renderer.blit(texture, dest_rect)


def resolve_collision(p1, p2):
    diff = p1.pos - p2.pos
    dist = diff.length()
    min_dist = (p1.base_w + p2.base_w) * 0.4
    if 0 < dist < min_dist:
        push = diff.normalize() * (min_dist - dist) * 0.5
        p1.pos += push
        p2.pos -= push


CX, CY = WIDTH // 2, HEIGHT // 2
parts = [
    JiggleOval(CX - 45, CY - 20, 85, 100),
    JiggleOval(CX + 45, CY - 20, 85, 100)
]

clock = pygame.time.Clock()
running = True

while running:
    m_pos = pygame.Vector2(pygame.mouse.get_pos())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for p in parts:
                if p.check_click(m_pos): break  # Захватываем только одну за раз
        if event.type == pygame.MOUSEBUTTONUP:
            for p in parts: p.is_dragging = False

    # Обновление
    for p in parts: p.update()
    resolve_collision(parts[0], parts[1])

    # Рендер
    rend.draw_color = (45, 45, 55, 255)
    rend.clear()

    # # Тело
    # rend.draw_color = (220, 220, 220, 255)
    # rend.fill_rect(pygame.Rect(CX - 80, CY - 60, 160, 200))
    # rend.fill_rect(pygame.Rect(CX - 35, CY - 135, 70, 70))

    for p in parts: p.draw(rend, circle_tex)

    rend.present()
    clock.tick(FPS)

pygame.quit()
