import pygame
from pygame._sdl2 import Window, Renderer, Texture

pygame.init()
WIDTH, HEIGHT = 1024, 768
pygame.display.set_mode((WIDTH, HEIGHT), pygame.HIDDEN)

sdl_win = Window("PyOS v2", (WIDTH, HEIGHT))
renderer = Renderer(sdl_win)
TASKBAR_HEIGHT = 45


class AppWindow:
    def __init__(self, title, x, y):
        self.title = title
        self.rect = pygame.FRect(x, y, 450, 320)
        self.stored_rect = pygame.FRect(x, y, 450, 320)
        self.angle = 0.0
        self.is_dragging = False
        self.is_maximized = False
        self.is_minimized = False
        self.closed = False

        # Текстура окна (800x600 для четкости)
        surf = pygame.Surface((800, 600))
        surf.fill((245, 245, 245))
        # Заголовок
        pygame.draw.rect(surf, (40, 40, 40), (0, 0, 800, 50))
        # Кнопки: Закрыть (X), Развернуть ([]), Свернуть (_)
        pygame.draw.rect(surf, (200, 50, 50), (740, 10, 50, 30))  # Close
        pygame.draw.rect(surf, (100, 100, 100), (680, 10, 50, 30))  # Max
        pygame.draw.rect(surf, (100, 100, 100), (620, 10, 50, 30))  # Min

        font = pygame.font.SysFont("Segoe UI", 28)
        surf.blit(font.render(title, True, (255, 255, 255)), (20, 7))

        # Заглушка проводника внутри
        for row in range(2):
            for col in range(4):
                pygame.draw.rect(surf, (200, 200, 200), (40 + col * 180, 80 + row * 150, 140, 100), 0, 5)

        self.texture = Texture.from_surface(renderer, surf)


windows = []
show_3d = False
clock = pygame.time.Clock()

# Иконка папки на рабочем столе
folder_rect = pygame.Rect(40, 40, 70, 70)
f_surf = pygame.Surface((70, 70), pygame.SRCALPHA)
pygame.draw.rect(f_surf, (255, 210, 50), (5, 15, 60, 45), 0, 5)
pygame.draw.rect(f_surf, (255, 230, 100), (5, 10, 30, 10), 0, 3)
folder_tex = Texture.from_surface(renderer, f_surf)

running = True
while running:
    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            show_3d = not show_3d

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Клик по кнопке Выключения (справа внизу)
            if mx > WIDTH - 50 and my > HEIGHT - TASKBAR_HEIGHT:
                running = False

            if not show_3d:
                # Клик по Панели задач (разворот конкретного окна)
                if my > HEIGHT - TASKBAR_HEIGHT:
                    idx = (mx - 100) // 60
                    if 0 <= idx < len(windows):
                        target_win = windows[int(idx)]
                        target_win.is_minimized = not target_win.is_minimized
                        if not target_win.is_minimized:  # На передний план при открытии
                            windows.append(windows.pop(int(idx)))

                # Клик по папке
                elif folder_rect.collidepoint(mx, my):
                    windows.append(
                        AppWindow(f"Folder {len(windows) + 1}", 200 + len(windows) * 30, 150 + len(windows) * 30))

                # Клик по окнам
                for w in reversed([win for win in windows if not win.is_minimized]):
                    if w.rect.collidepoint(mx, my):
                        windows.remove(w);
                        windows.append(w)  # Focus
                        rel_x = (mx - w.rect.x) * (800 / w.rect.width)
                        rel_y = (my - w.rect.y) * (600 / w.rect.height)
                        if rel_y < 50:
                            if rel_x > 740:
                                w.closed = True
                            elif rel_x > 680:
                                w.is_maximized = not w.is_maximized
                            elif rel_x > 620:
                                w.is_minimized = True
                            else:
                                w.is_dragging = True
                        break

        if event.type == pygame.MOUSEBUTTONUP:
            for w in windows: w.is_dragging = False

        if event.type == pygame.MOUSEMOTION:
            if not show_3d:
                for w in windows:
                    if w.is_dragging and not w.is_maximized:
                        w.stored_rect.x += event.rel[0]
                        w.stored_rect.y += event.rel[1]

    windows = [w for w in windows if not w.closed]

    renderer.draw_color = (0, 90, 160)
    renderer.clear()
    folder_tex.draw(dstrect=folder_rect)

    # Отрисовка окон с анимацией
    for i, w in enumerate(windows):
        if show_3d:
            spacing = WIDTH / (len(windows) + 1)
            tx, ty, tw, th, tang = (i + 1) * spacing - 150, HEIGHT // 2 - 110, 300, 225, -25.0
        elif w.is_minimized:
            tx, ty, tw, th, tang = 100 + i * 60, HEIGHT, 40, 0, 0
        elif w.is_maximized:
            tx, ty, tw, th, tang = 0, 0, WIDTH, HEIGHT - TASKBAR_HEIGHT, 0
        else:
            tx, ty, tw, th, tang = w.stored_rect.x, w.stored_rect.y, w.stored_rect.width, w.stored_rect.height, 0

        w.rect.x += (tx - w.rect.x) * 0.15
        w.rect.y += (ty - w.rect.y) * 0.15
        w.rect.width += (tw - w.rect.width) * 0.15
        w.rect.height += (th - w.rect.height) * 0.15
        w.angle += (tang - w.angle) * 0.15

        if w.rect.height > 2:
            w.texture.draw(dstrect=w.rect, angle=w.angle)

    # Панель задач
    renderer.draw_color = (15, 15, 15)
    renderer.fill_rect((0, HEIGHT - TASKBAR_HEIGHT, WIDTH, TASKBAR_HEIGHT))

    # Отрисовка иконок (теперь они СТАТИЧНЫ по индексу, не прыгают)
    for i, w in enumerate(windows):
        color = (0, 120, 215) if not w.is_minimized else (60, 60, 60)
        renderer.draw_color = color
        renderer.fill_rect((100 + i * 60, HEIGHT - 35, 45, 25))

    # Кнопка Power
    renderer.draw_color = (200, 0, 0)
    renderer.fill_rect((WIDTH - 40, HEIGHT - 35, 30, 25))

    renderer.present()
    clock.tick(60)

pygame.quit()
