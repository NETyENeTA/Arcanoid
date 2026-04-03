import pygame
import math

WIDTH, HEIGHT = 800, 600
FOV = 400


class Cube:
    def __init__(self, size, color):
        self.color = color
        s = size / 2
        # Вершины
        self.vertices = [
            [-s, -s, -s], [s, -s, -s], [s, s, -s], [-s, s, -s],
            [-s, -s, s], [s, -s, s], [s, s, s], [-s, s, s]
        ]
        # Грани (индексы вершин)
        self.faces = [
            (0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4),
            (2, 3, 7, 6), (0, 3, 7, 4), (1, 2, 6, 5)
        ]

    def get_transformed_faces(self, angle, offset_z):
        faces_data = []
        rotated_vertices = []

        # Вращение и проекция
        for v in self.vertices:
            x, y, z = v
            # Rotate Y
            nx = x * math.cos(angle) + z * math.sin(angle)
            nz = -x * math.sin(angle) + z * math.cos(angle)
            x, z = nx, nz
            # Rotate X
            ny = y * math.cos(angle * 0.5) - z * math.sin(angle * 0.5)
            nz = y * math.sin(angle * 0.5) + z * math.cos(angle * 0.5)
            y, z = ny, nz + offset_z

            f = FOV / z
            rotated_vertices.append((x * f + WIDTH // 2, y * f + HEIGHT // 2, z))

        for face in self.faces:
            pts = [rotated_vertices[i] for i in face]
            # Векторное произведение для определения лицевой/обратной стороны
            # (x2-x1)*(y3-y1) - (y2-y1)*(x3-x1)
            v_prod = (pts[1][0] - pts[0][0]) * (pts[2][1] - pts[0][1]) - \
                     (pts[1][1] - pts[0][1]) * (pts[2][0] - pts[0][0])

            avg_z = sum(p[2] for p in pts) / 4
            faces_data.append({
                'pts': [(p[0], p[1]) for p in pts],
                'z': avg_z,
                'is_front': v_prod > 0  # True если грань смотрит на камеру
            })
        return faces_data


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    outer = Cube(300, (60, 60, 100))
    inner = Cube(100, (200, 50, 50))

    angle = 0
    while True:
        if pygame.event.peek(pygame.QUIT): return
        screen.fill((20, 20, 25))
        angle += 0.02

        # Получаем данные граней
        outer_faces = outer.get_transformed_faces(angle, 600)
        inner_faces = inner.get_transformed_faces(angle * 1.5, 600)

        # 1. Рисуем ЗАДНИЕ грани внешнего куба (те, что внутри коробки)
        for f in sorted([f for f in outer_faces if not f['is_front']], key=lambda x: x['z'], reverse=True):
            pygame.draw.polygon(screen, (30, 30, 50), f['pts'])
            pygame.draw.polygon(screen, (80, 80, 150), f['pts'], 1)

        # 2. Рисуем ПЕРЕДНИЕ грани внутреннего куба (по твоему условию)
        for f in sorted([f for f in inner_faces if f['is_front']], key=lambda x: x['z'], reverse=True):
            pygame.draw.polygon(screen, inner.color, f['pts'])
            pygame.draw.polygon(screen, (255, 255, 255), f['pts'], 1)

        # 3. Рисуем ПЕРЕДНИЕ грани внешнего куба (внешняя оболочка)
        # Делаем их полупрозрачными или просто контуром, чтобы видеть внутренности
        for f in sorted([f for f in outer_faces if f['is_front']], key=lambda x: x['z'], reverse=True):
            # В pygame отрисовка прозрачности требует отдельного Surface,
            # поэтому здесь просто рисуем сетку для наглядности
            pygame.draw.polygon(screen, (100, 100, 255), f['pts'], 2)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
