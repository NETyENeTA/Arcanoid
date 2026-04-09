import pygame as pg


class Timer:
    def __init__(self, pause: bool = False):
        self._start_tick = pg.time.get_ticks()
        self._paused_tick = self._start_tick if pause else 0
        self._is_paused = pause

    @property
    def total_ms(self):
        if self._is_paused:
            # Если на паузе, отдаем время, которое зафиксировали при остановке
            return self._paused_tick - self._start_tick
        # Если играем, вычитаем старт из текущего времени
        return pg.time.get_ticks() - self._start_tick

    @property
    def is_paused(self):
        return self._is_paused

    def switch_pause(self, pause: bool):

        if self._is_paused == pause:
            return

        self.toggle_pause()

    def toggle_pause(self):
        if self._is_paused:
            # Снимаем с паузы: вычисляем, сколько простояли
            pause_duration = pg.time.get_ticks() - self._paused_tick
            # Сдвигаем старт вперед, чтобы время паузы "выпало" из счета
            self._start_tick += pause_duration
            self._is_paused = False
        else:
            # Ставим на паузу: запоминаем "момент заморозки"
            self._paused_tick = pg.time.get_ticks()
            self._is_paused = True

    @property
    def s(self):
        return (self.total_ms // 1000) % 60

    @property
    def m(self):
        return (self.total_ms // 60000) % 60

    @property
    def h(self):
        return self.total_ms // 3600000

    def get_format(self, format_time="%h%:%m%:%s%"):
        return (format_time.lower()
                .replace("%h%", f"{self.h:02}")
                .replace("%m%", f"{self.m:02}")
                .replace("%s%", f"{self.s:02}"))

    def get(self, show_hours=False) -> str:
        """Возвращает строку вида 01:25 или 00:01:25"""
        if show_hours or self.h > 0:
            return f"{self.h:02}:{self.m:02}:{self.s:02}"
        return f"{self.m:02}:{self.s:02}"
