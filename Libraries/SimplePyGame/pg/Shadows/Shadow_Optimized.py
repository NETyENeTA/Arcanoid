from core.App import AppConfigs as App, pg


class ShadowCaster:
    def init_shadow(self):
        # 1. Белая заготовка (наш холст)
        self._shadow_mask = pg.Surface(self.hitbox.size, pg.SRCALPHA)
        self.draw_shadow_shape(self._shadow_mask, (255, 255, 255, 255))

        # 2. Создаем отдельный буфер для финальной тени, чтобы не создавать его в цикле
        self._shadow_final = pg.Surface(self.hitbox.size, pg.SRCALPHA)

    def cast_shadow(self):
        for light in App.Lights:
            direction = self.center - light.pos
            dist = direction.magnitude

            if dist > 0:
                # Твой расчет offset и alpha
                offset = direction.normalized * max(self.shadow_info.minimal,
                                                    min(dist * self.shadow_info.middle, self.shadow_info.maximal))
                alpha_val = max(0, min(160, 180 - int(dist * 0.3)))

                # --- ЦВЕТОВАЯ МАГИЯ ---

                # СИЛЬНО затемняем цвет лампы, чтобы он стал "ТЕНЬЮ" (видной на белом)
                # Коэффициент 0.2 - 0.4 даст глубокий темный оттенок цвета
                dark_factor = 0.3
                shadow_rgb = (
                    int(light.color.r * dark_factor),
                    int(light.color.g * dark_factor),
                    int(light.color.b * dark_factor)
                )

                # 1. Очищаем финальный буфер
                self._shadow_final.fill((0, 0, 0, 0))

                # 2. Заливаем буфер темным цветом лампы с нужной альфой
                self._shadow_final.fill((*shadow_rgb, alpha_val))

                # 3. Накладываем БЕЛУЮ маску через MULT (оставляем только форму объекта)
                # Белый (255) сохранит цвет, прозрачный (0) — обрежет лишнее
                self._shadow_final.blit(self._shadow_mask, (0, 0), special_flags=pg.BLEND_RGBA_MULT)

                # 4. Рисуем на экран
                self.screen.blit(self._shadow_final, (self.pos + offset).xy)


