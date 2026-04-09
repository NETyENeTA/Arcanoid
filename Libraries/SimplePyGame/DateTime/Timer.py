from DateTime.Stopwatch import Stopwatch


class Timer(Stopwatch):
    def __init__(self, seconds: int, pause: bool = False):
        super().__init__(pause=pause)
        self._limit_ms = seconds * 1000  # Переводим заданное время в мс

    @property
    def total_ms(self):
        # Берем время из родительского Stopwatch
        elapsed = super().total_ms
        # Вычитаем из лимита прошедшее время
        remaining = self._limit_ms - elapsed
        return max(0, remaining)  # Чтобы не уходило в минус

    @property
    def is_finished(self):
        return self.total_ms <= 0
