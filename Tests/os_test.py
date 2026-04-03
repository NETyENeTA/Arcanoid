import pygame
from pygame._sdl2 import Window, Renderer, Texture
import time

pygame.init()
WIDTH, HEIGHT = 1024, 768
pygame.display.set_mode((WIDTH, HEIGHT), pygame.HIDDEN)

sdl_win = Window("PyOS v3", (WIDTH, HEIGHT))
renderer = Renderer(sdl_win)
TASKBAR_HEIGHT = 45


class AppWindow:
    def __init__(self, title, x, y, id_num):
        self.id = id_num
        self.title = title
        self.rect = pygame.FRect(x, y, 0, 0)
        self.stored_rect = pygame.FRect(WIDTH // 2 - 225, HEIGHT // 2 - 160, 450, 320)
        self.angle = 0.0
        self.alpha = 0.0
        self.is_dragging = False
        self.is_maximized = False
        self.is_minimized = False
        self.closed = False

        surf = pygame.Surface((800, 600))
        surf.fill((245, 245, 245))
        pygame.draw.rect(surf, (45, 45, 48), (0, 0, 800, 50))
        f = pygame.font.SysFont("Arial", 24)
        pygame.draw.rect(surf, (200, 60, 60), (740, 10, 50, 30))
        pygame.draw.rect(surf, (100, 100, 100), (680, 10, 50, 30))
        pygame.draw.rect(surf, (70, 70, 70), (620, 10, 50, 30))
        surf.blit(f.render("x", True, (255, 255, 255)), (755, 10))
        surf.blit(f.render("o", True, (255, 255, 255)), (695, 10))
        surf.blit(f.render("-", True, (255, 255, 255)), (638, 5))
        font = pygame.font.SysFont("Segoe UI", 28)
        surf.blit(font.render(title, True, (255, 255, 255)), (20, 7))

        self.texture = Texture.from_surface(renderer, surf)
        self.texture.blend_mode = 1

        shadow_size = (840, 640)
        s_surf = pygame.Surface(shadow_size, pygame.SRCALPHA)
        for i in range(20, 0, -2):
            alpha = 40 - (i * 2)
            pygame.draw.rect(s_surf, (0, 0, 0, max(0, alpha)), (20 - i, 20 - i, 800 + i * 2, 600 + i * 2), 0, 15)
        self.shadow_tex = Texture.from_surface(renderer, s_surf)
        self.shadow_tex.blend_mode = 1


# Состояния системы
windows = []
taskbar_order = []
active_window = None
show_3d = False

# Плавный скролл
scroll_offset = 0
target_scroll = 0

# Загрузка и выключение
booting = True
boot_progress = 0
boot_alpha = 255
shutting_down = False
shutdown_fade = 0

show_start_menu = False
start_menu_rect = pygame.FRect(10, HEIGHT, 300, 400)
bg_color = (0, 80, 150)
blur_alpha = 0
clock = pygame.time.Clock()
font_ui = pygame.font.SysFont("Segoe UI", 16)
last_time_str = ""
time_tex = None

folder_rect = pygame.FRect(40, 40, 70, 70)
folder_dragging = False
last_folder_click_time = 0
f_surf = pygame.Surface((70, 70), pygame.SRCALPHA)
pygame.draw.rect(f_surf, (255, 210, 50), (5, 15, 60, 45), 0, 5)
folder_tex = Texture.from_surface(renderer, f_surf)

blur_surf = pygame.Surface((WIDTH, HEIGHT))
blur_surf.fill((0, 0, 0))
blur_tex = Texture.from_surface(renderer, blur_surf)
blur_tex.blend_mode = 1


def draw_dashed_line(renderer, x1, y, x2):
    for i in range(int(x1), int(x2), 6):
        renderer.draw_line((i, y), (min(i + 3, x2), y))


running = True
while running:
    mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

        if not booting:  # Блокируем ввод во время загрузки
            if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                show_3d = not show_3d
                target_scroll = 0

            if event.type == pygame.MOUSEWHEEL and show_3d:
                target_scroll += event.y * 200

            if event.type == pygame.MOUSEBUTTONDOWN and not shutting_down:
                clicked_any = False

                # КЛИК ПО ПУСКУ
                if 15 < mx < 55 and HEIGHT - 35 < my < HEIGHT - 10:
                    show_start_menu = not show_start_menu
                    clicked_any = True
                elif show_start_menu:
                    # Кнопка ВЫХОД
                    exit_btn = pygame.Rect(start_menu_rect.x + 10, start_menu_rect.bottom - 50,
                                           start_menu_rect.width - 20, 40)
                    if exit_btn.collidepoint(mx, my):
                        shutting_down = True
                        clicked_any = True
                    elif not start_menu_rect.collidepoint(mx, my):
                        show_start_menu = False

                # ПАПКА
                if not clicked_any and folder_rect.collidepoint(mx, my) and not show_3d:
                    curr_time = pygame.time.get_ticks()
                    if curr_time - last_folder_click_time < 300:
                        new_win = AppWindow(f"Folder {len(taskbar_order) + 1}", folder_rect.x, folder_rect.y,
                                            len(taskbar_order))
                        windows.append(new_win)
                        taskbar_order.append(new_win)
                        active_window = new_win
                    else:
                        folder_dragging = True
                        last_folder_click_time = curr_time
                    clicked_any = True

                # КЛИКИ ПО ОКНАМ
                if not clicked_any:
                    for w in reversed([win for win in windows if not win.is_minimized and not win.closed]):
                        if w.rect.collidepoint(mx, my):
                            active_window = w
                            windows.remove(w)
                            windows.append(w)
                            rel_x = (mx - w.rect.x) * (800 / w.rect.width) if w.rect.width > 0 else 0
                            rel_y = (my - w.rect.y) * (600 / w.rect.height) if w.rect.height > 0 else 0
                            if rel_y < 50:
                                if rel_x > 740:
                                    w.closed = True
                                    if w in taskbar_order: taskbar_order.remove(w)
                                elif rel_x > 680:
                                    w.is_maximized = not w.is_maximized
                                elif rel_x > 620:
                                    w.is_minimized = True
                                    active_window = None
                                else:
                                    w.is_dragging = True
                            clicked_any = True
                            break

                # ПАНЕЛЬ ЗАДАЧ
                if not clicked_any and my > HEIGHT - TASKBAR_HEIGHT:
                    idx = (mx - 100) // 60
                    if 0 <= idx < len(taskbar_order):
                        w = taskbar_order[int(idx)]
                        if w == active_window:
                            w.is_minimized = True
                            active_window = None
                        else:
                            w.is_minimized = False
                            if w in windows: windows.remove(w)
                            windows.append(w)
                            active_window = w
                        clicked_any = True

                if not clicked_any: active_window = None

        if event.type == pygame.MOUSEBUTTONUP:
            folder_dragging = False
            for w in windows: w.is_dragging = False

        if event.type == pygame.MOUSEMOTION and not booting:
            if folder_dragging:
                folder_rect.x += event.rel[0]
                folder_rect.y += event.rel[1]
            for w in windows:
                if w.is_dragging and not w.is_maximized:
                    w.stored_rect.x += event.rel[0]
                    w.stored_rect.y += event.rel[1]

    # --- ЛОГИКА СКРОЛЛА (LERP + ОГРАНИЧЕНИЕ) ---
    max_s = max(0, (len(taskbar_order) - 1) * 450)
    if target_scroll > 0: target_scroll += (0 - target_scroll) * 0.2
    if target_scroll < -max_s: target_scroll += (-max_s - target_scroll) * 0.2
    scroll_offset += (target_scroll - scroll_offset) * 0.15

    # РЕНДЕРИНГ
    renderer.draw_color = bg_color
    renderer.clear()
    folder_tex.draw(dstrect=folder_rect)

    target_blur = 160 if (show_3d or show_start_menu) else 0
    blur_alpha += (target_blur - blur_alpha) * 0.1
    if blur_alpha > 1:
        blur_tex.alpha = int(blur_alpha)
        blur_tex.draw()

    # ОТРИСОВКА ОКОН
    for w in (list(windows) if not show_3d else sorted(windows, key=lambda x: taskbar_order.index(
            x) if x in taskbar_order else 0)):
        if w.closed:
            tx, ty, tw, th, tang, alpha = w.rect.centerx, w.rect.centery, 0, 0, 0, 0
            if w.rect.width < 10:
                if w in windows: windows.remove(w)
                continue
        elif show_3d:
            idx = taskbar_order.index(w) if w in taskbar_order else 0
            tx = (WIDTH // 2 - 200) + (idx * 450) + scroll_offset
            dist = abs((tx + 200) - WIDTH / 2)
            scale = max(0.4, 1.0 - (dist / 800))
            ty, tw, th, tang, alpha = (HEIGHT // 2 - 150) + (
                        300 - 300 * scale) / 2, 400 * scale, 300 * scale, -15.0, max(30, 255 - int(dist / 1.5))
        elif w.is_minimized:
            idx = taskbar_order.index(w) if w in taskbar_order else 0
            tx, ty, tw, th, tang, alpha = 100 + idx * 60, HEIGHT, 45, 0, 0, 0
        elif w.is_maximized:
            tx, ty, tw, th, tang, alpha = 0, 0, WIDTH, HEIGHT - TASKBAR_HEIGHT, 0, 255
        else:
            tx, ty, tw, th, tang, alpha = w.stored_rect.x, w.stored_rect.y, w.stored_rect.width, w.stored_rect.height, 0, 255

        w.rect.x += (tx - w.rect.x) * 0.15
        w.rect.y += (ty - w.rect.y) * 0.15
        w.rect.width += (tw - w.rect.width) * 0.15
        w.rect.height += (th - w.rect.height) * 0.15
        w.angle += (tang - w.angle) * 0.15
        w.alpha += (alpha - w.alpha) * 0.15

        if w.rect.height > 5:
            current_alpha = int(w.alpha if w == active_window or show_3d else w.alpha * 0.7)
            if not w.is_minimized and not w.is_maximized:
                s_rect = pygame.FRect(w.rect.x - 15, w.rect.y - 5, w.rect.width + 30, w.rect.height + 40)
                w.shadow_tex.alpha = int(current_alpha * 0.5)
                w.shadow_tex.draw(dstrect=s_rect, angle=w.angle)
            w.texture.alpha = max(0, min(255, int(w.alpha)))
            w.texture.draw(dstrect=w.rect, angle=w.angle)


    # МЕНЮ ПУСК
    target_start_y = HEIGHT - TASKBAR_HEIGHT - 400 if show_start_menu else HEIGHT
    start_menu_rect.y += (target_start_y - start_menu_rect.y) * 0.2
    renderer.draw_color = (30, 30, 35)
    renderer.fill_rect(start_menu_rect)

    if start_menu_rect.y < HEIGHT:
        renderer.draw_color = (200, 60, 60)
        renderer.fill_rect((start_menu_rect.x + 10, start_menu_rect.bottom - 50, start_menu_rect.width - 20, 40))
        btn_f = font_ui.render("Выход", True, (255, 255, 255))
        btn_tex = Texture.from_surface(renderer, btn_f)
        btn_tex.draw(dstrect=(start_menu_rect.x + 120, start_menu_rect.bottom - 40, btn_tex.width, btn_tex.height))

    # ИНТЕРФЕЙС
    renderer.draw_color = (15, 15, 20)
    renderer.fill_rect((0, HEIGHT - TASKBAR_HEIGHT, WIDTH, TASKBAR_HEIGHT))
    renderer.draw_color = (0, 120, 215)
    renderer.fill_rect((15, HEIGHT - 35, 40, 25))

    for i, w in enumerate(taskbar_order):
        rx, ry, rw, rh = 100 + i * 60, HEIGHT - 35, 45, 25
        ind_y = HEIGHT - 6
        if w == active_window:
            renderer.draw_color = (60, 60, 70);
            renderer.fill_rect((rx, ry, rw, rh))
            renderer.draw_color = (0, 120, 215);
            renderer.fill_rect((rx, ind_y, rw, 3))
        elif w.is_minimized:
            renderer.draw_color = (35, 35, 40);
            renderer.fill_rect((rx, ry, rw, rh))
            renderer.draw_color = (120, 120, 120);
            draw_dashed_line(renderer, rx, ind_y, rx + rw)
        else:
            renderer.draw_color = (45, 45, 50);
            renderer.fill_rect((rx, ry, rw, rh))
            renderer.draw_color = (100, 100, 100);
            renderer.fill_rect((rx, ind_y, rw, 2))

    # ВРЕМЯ
    cur_time = time.strftime("%H:%M")
    if cur_time != last_time_str:
        last_time_str = cur_time
        t_s = font_ui.render(cur_time, True, (255, 255, 255))
        time_tex = Texture.from_surface(renderer, t_s)
    if time_tex:
        time_tex.draw(dstrect=(WIDTH - time_tex.width - 15, HEIGHT - 32, time_tex.width, time_tex.height))

    # --- ЭКРАН ЗАГРУЗКИ ---
    if booting:
        renderer.draw_color = (10, 10, 15)
        renderer.fill_rect((0, 0, WIDTH, HEIGHT))
        logo_f = pygame.font.SysFont("Segoe UI", 50, bold=True)
        l_s = logo_f.render("PyOS v3", True, (255, 255, 255))
        l_t = Texture.from_surface(renderer, l_s)
        l_t.draw(dstrect=(WIDTH // 2 - l_t.width // 2, HEIGHT // 2 - 60, l_t.width, l_t.height))

        boot_progress += 2
        renderer.draw_color = (50, 50, 60);
        renderer.draw_rect((WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 6))
        renderer.draw_color = (0, 120, 215);
        renderer.fill_rect((WIDTH // 2 - 100, HEIGHT // 2 + 20, min(200, int(boot_progress)), 6))

        if boot_progress > 250:
            boot_alpha -= 10
            if boot_alpha <= 0: booting = False
        if boot_alpha < 255:
            blur_tex.alpha = 255 - max(0, boot_alpha);
            blur_tex.draw()

    # --- ЭФФЕКТ ВЫКЛЮЧЕНИЯ ---
    if shutting_down:
        shutdown_fade += 7
        if shutdown_fade > 255: running = False
        blur_tex.alpha = min(255, shutdown_fade);
        blur_tex.draw()

    renderer.present()
    clock.tick(60)

pygame.quit()
