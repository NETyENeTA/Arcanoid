import pygame
import math
import random


class SpaceRenderer:
    def __init__(self, rend, width, height):
        self.rend = rend
        self.W, self.H = width, height

    def project(self, pos, cam, sy, cy, sp, cp, fov, shake):
        tx, ty, tz = pos[0] - cam[0], pos[1] - cam[1], pos[2] - cam[2]
        rx, rz = tx * cy - tz * sy, tx * sy + tz * cy
        ry, rz = ty * cp - rz * sp, ty * sp + rz * cp
        if rz <= 10: return None
        f = fov / rz
        return (int(rx * f + self.W // 2 + shake), int(ry * f + self.H // 2 + shake), rz, f)

    def draw_stars(self, stars, cam, vel, sy, cy, sp, cp, fov, shake, speed):
        for s in stars:
            p1 = self.project(s, cam, sy, cy, sp, cp, fov, shake)
            if p1:
                # Эффект варпа: вычисляем положение хвоста
                t = 0.0001 + speed * 0.00012
                s2 = [s[0] - vel[0] * t, s[1] - vel[1] * t, s[2] - vel[2] * t]
                p2 = self.project(s2, cam, sy, cy, sp, cp, fov, shake)

                sh = int(min(255, 140 + speed * 0.05))
                self.rend.draw_color = (sh, sh, 255, 200)
                if p2:
                    # Передаем два кортежа (x,y)
                    self.rend.draw_line((p1[0], p1[1]), (p2[0], p2[1]))
                else:
                    self.rend.fill_rect(pygame.Rect(p1[0], p1[1], 1, 1))

    def draw_radar(self, planets, cam, target, scale=0.05):
        rx, ry, size = self.W - 130, self.H - 130, 100
        self.rend.draw_color = (40, 60, 80, 150)
        self.rend.draw_line((rx - size, ry), (rx + size, ry))
        self.rend.draw_line((rx, ry - size), (rx, ry + size))
        for p in planets:
            dx, dz = (p.pos[0] - cam[0]) * scale, (p.pos[2] - cam[2]) * scale
            if abs(dx) < size and abs(dz) < size:
                is_t = (p == target)
                self.rend.draw_color = (*p.color, 255 if is_t else 150)
                s = 4 if is_t else 2
                self.rend.fill_rect(pygame.Rect(int(rx + dx - s // 2), int(ry + dz - s // 2), s, s))
        self.rend.draw_color = (255, 255, 255, 255)
        self.rend.fill_rect(pygame.Rect(rx - 2, ry - 2, 4, 4))
