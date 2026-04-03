import pygame as pg

from Libraries.SimplePyGame.Positions import Vec2


class SFXSystem:

    class Modes:
        Left = 0
        Right = 1

    def __init__(self, width: int, master_volume=0.6):
        self.sounds = {}
        self.master_volume = master_volume
        self.width = width

    def load(self, name, path):
        """Загружает звук в словарь один раз"""
        self.sounds[name] = pg.mixer.Sound(path)

    def play(self, name):
        """Обычное воспроизведение по центру (стерео 1.0 : 1.0)"""
        sound = self.sounds.get(name)
        if sound:
            # Просто находим любой свободный канал и играем с мастер-громкостью
            channel = pg.mixer.find_channel()
            if channel:
                # channel.set_volume(self.master_volume)
                channel.set_volume(self.master_volume, self.master_volume)
                channel.play(sound)

    def mode_play(self, name, mode: Modes | int):

        sound = self.sounds.get(name)
        if sound:
            channel = pg.mixer.find_channel()
            if channel:
                direction = Vec2(0, 0)
                if mode == SFXSystem.Modes.Left:
                    direction.x = 1
                elif mode == SFXSystem.Modes.Right:
                    direction.y = 1

                direction *= self.master_volume
                channel.set_volume(direction.x, direction.y)
                channel.play(sound)




    def pos_play(self, name, x_pos, screen_width: int | None = None):
        """Воспроизведение с привязкой к позиции X (панорама)"""
        sound = self.sounds.get(name)
        if sound:
            channel = pg.mixer.find_channel()
            if channel:
                # Выбираем ширину: либо переданную, либо системную
                w = screen_width if screen_width else self.width

                # Считаем коэффициент (от 0.0 до 1.0)
                # Добавим clamp (0.1 - 0.9), чтобы звук не пропадал совсем в одном ухе
                panning = max(0.1, min(0.9, x_pos / w if w > 0 else 0.5))

                # Рассчитываем громкость для каждого уха
                left_vol = (1.0 - panning) * self.master_volume
                right_vol = panning * self.master_volume

                # Устанавливаем баланс и играем
                channel.set_volume(left_vol, right_vol)
                channel.play(sound)
