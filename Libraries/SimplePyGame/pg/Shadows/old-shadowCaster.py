

class ShadowCaster:

    def cast_shadow(self):
        for light in App.Lights:
            # Расчет вектора (твой стандартный блок)
            direction = self.center - light.pos
            dist = direction.magnitude

            if dist > 0:
                shadow_len = max(self.shadow_info.minimal,
                                 min(dist * self.shadow_info.middle,
                                     self.shadow_info.maximal))
                offset = direction.normalized * shadow_len

                # Позиция отрисовки тени
                # (используем смещение от базовой позиции объекта)
                render_pos = self.pos + offset

                # --- МАГИЯ ALPHA ---
                # 1. Создаем пустую прозрачную поверхность по размеру хитбокса
                temp_surf = pg.Surface(self.hitbox.size, pg.SRCALPHA)

                # 2. Вычисляем прозрачность затухания
                alpha_val = max(0, min(160, 180 - int(dist * 0.3)))
                shadow_color = (*light.color.rgb, alpha_val)  # Черная тень с альфой

                # 3. КЛЮЧЕВОЙ МОМЕНТ: вызываем метод отрисовки формы
                # Мы передаем temp_surf и локальные координаты (0, 0)
                self.draw_shadow_shape(temp_surf, shadow_color)

                # 4. Переносим готовую мягкую тень на основной экран
                self.screen.blit(temp_surf, render_pos.xy)
