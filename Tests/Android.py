import pygame
import time
import psutil  # Для получения заряда батареи
from pygame._sdl2.video import Window, Renderer, Texture

WIDTH, HEIGHT = 360, 640
pygame.init()

win = Window("Android Real Battery OS", size=(WIDTH, HEIGHT))
renderer = Renderer(win)
font = pygame.font.SysFont("Arial", 14, bold=True)


def create_tex(color, size=(60, 60), alpha=255, radius=12):
    surf = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.rect(surf, (*color, alpha), (0, 0, *size), border_radius=radius)
    return Texture.from_surface(renderer, surf)


# Текстуры
wallpaper = create_tex((25, 30, 45), (WIDTH, HEIGHT), radius=0)
shade_tex = create_tex((15, 15, 20), (WIDTH, HEIGHT), alpha=245, radius=0)
icon_tex = create_tex((70, 130, 250))
app_window = create_tex((35, 35, 40), (WIDTH, HEIGHT), radius=0)

# Состояния
scroll_x, target_page = 0.0, 0
shade_y = -float(HEIGHT)
app_open_val = 0.0
is_dragging_shade = False
is_dragging_page = False
active_app = False

clock = pygame.time.Clock()
running = True

while running:
    mx, my = pygame.mouse.get_pos()

    # 1. ПОЛУЧАЕМ ДАННЫЕ О БАТАРЕЕ (в реальном времени)
    battery = psutil.sensors_battery()
    if battery:
        percent = battery.percent
        is_charging = battery.power_plugged
    else:
        percent, is_charging = 100, False  # Если ПК без батареи

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if my < 30:
                is_dragging_shade = True
            elif my > HEIGHT - 40:
                active_app = False  # Home
            elif not active_app:
                is_dragging_page = True
                start_mx, start_sx = mx, scroll_x

        if event.type == pygame.MOUSEBUTTONUP:
            if is_dragging_page:
                if abs(mx - start_mx) < 5: active_app = True
                is_dragging_page = False
            is_dragging_shade = False
            target_page = max(0, min(2, round(-scroll_x / WIDTH)))

    # --- ЛОГИКА АНИМАЦИЙ ---
    target_shade = 0 if (is_dragging_shade and my > HEIGHT / 2) or (
                not is_dragging_shade and shade_y > -HEIGHT / 2) else -HEIGHT
    shade_y += ((my - HEIGHT if is_dragging_shade else target_shade) - shade_y) * 0.15

    if is_dragging_page:
        scroll_x = start_sx + (mx - start_mx)
    else:
        scroll_x += (-target_page * WIDTH - scroll_x) * 0.15

    app_open_val += ((1.0 if active_app else 0.0) - app_open_val) * 0.15

    # --- РЕНДЕР (GPU) ---
    renderer.clear()
    wallpaper.draw()

    # Рабочие столы + Индикаторы (Dots)
    for i in range(3):
        x_off = int(scroll_x + i * WIDTH)
        if -WIDTH < x_off < WIDTH:
            for r in range(3):
                for c in range(3): icon_tex.draw(dstrect=(x_off + 50 + c * 100, 100 + r * 120, 60, 60))

    for i in range(3):
        renderer.draw_color = (255, 255, 255, 255 if i == target_page else 80)
        renderer.fill_rect((WIDTH // 2 - 35 + i * 30, HEIGHT - 80, 10, 10))

    # Окно приложения
    if app_open_val > 0.01:
        aw, ah = int(WIDTH * app_open_val), int(HEIGHT * app_open_val)
        app_window.draw(dstrect=((WIDTH - aw) // 2, (HEIGHT - ah) // 2, aw, ah))

    # Статус-бар + БАТАРЕЯ
    renderer.draw_color = (0, 0, 0, 100)
    renderer.fill_rect((0, 0, WIDTH, 26))

    # Часы
    t_surf = font.render(time.strftime("%H:%M"), True, (255, 255, 255))
    Texture.from_surface(renderer, t_surf).draw(dstrect=(10, 5, 35, 16))

    # Иконка батареи
    renderer.draw_color = (255, 255, 255, 100)
    renderer.draw_rect((WIDTH - 45, 7, 24, 12))  # Корпус

    # Цвет полоски: синий (зарядка), красный (мало), зеленый (ок)
    if is_charging:
        b_color = (100, 200, 255, 255)
    elif percent < 20:
        b_color = (255, 100, 100, 255)
    else:
        b_color = (100, 255, 100, 255)

    renderer.draw_color = b_color
    fill_w = int(20 * (percent / 100))
    renderer.fill_rect((WIDTH - 43, 9, fill_w, 8))

    # Шторка и Навбар
    shade_tex.draw(dstrect=(0, int(shade_y), WIDTH, HEIGHT))
    renderer.draw_color = (0, 0, 0, 255)
    renderer.fill_rect((0, HEIGHT - 40, WIDTH, 40))
    renderer.draw_color = (255, 255, 255, 200)
    renderer.fill_rect((WIDTH // 2 - 20, HEIGHT - 25, 40, 8))

    renderer.present()
    clock.tick(60)

pygame.quit()
