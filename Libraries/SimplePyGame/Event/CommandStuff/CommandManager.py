from pygame.time import get_ticks
from Event.CommandStuff.Task import Task


class CommandManager:
    def __init__(self):
        self._tasks: list[Task] = []

    def add(self, command, delay: float, loops: int = 1):
        task = Task(command, delay, loops)
        self._tasks.append(task)
        return task  # Возвращаем таск, если захотим его удалить вручную

    def update(self):
        now = get_ticks()
        # Фильтруем список: оставляем только те, что не завершены
        for task in self._tasks[:]:
            task.update(now)
            if task.is_finished:
                self._tasks.remove(task)

    def clear(self):
        """Очистить все задачи (например, при смене уровня)"""
        self._tasks.clear()


def main():
    pass


if __name__ == "__main__":
    main()
