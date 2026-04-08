from pygame.time import get_ticks


class Task:
    def __init__(self, command, delay: float, loops: int):
        self.Command = command
        self.delay_ms = int(delay * 1000)
        self.loops = loops  # 0 для бесконечности, 1+ для счетчика
        self.deadline = get_ticks() + self.delay_ms
        self.is_finished = False

    def __repr__(self):
        return (f"Task({self.Command}, delay ms:{self.delay_ms}, loops:{self.loops}, deadline={self.deadline} "
                f"finished={self.is_finished})")

    def __str__(self):
        return (f"Task({self.Command}, delay ms:{self.delay_ms}, loops:{self.loops}, deadline={self.deadline} "
                f"finished={self.is_finished})")

    def update(self, now: int):
        if now >= self.deadline:
            # Выполняем команду
            self.Command()

            # Проверяем циклы
            if self.loops > 1:
                self.loops -= 1
                self.deadline = now + self.delay_ms
            elif self.loops == 0:  # Бесконечно
                self.deadline = now + self.delay_ms
            else:
                self.is_finished = True


def main():
    pass


if __name__ == "__main__":
    main()
