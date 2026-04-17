from typing import Callable

from DateTime.Timer import Timer
from DateTime.Task import Task, Command


class TimerExecutable(Timer):


    def __init__(self, seconds, command:Command | Callable, tasks: list[Task] = None, pause=False):
        super().__init__(seconds, pause)

        self.Command = command if isinstance(command, Command) else Command(command)
        self.Tasks = tasks or []


    def update(self):
        if self.is_paused:
            return

        if self.total_ms <= 0:
            self.switch_pause(True)
            self.Command.invoke()

        for task in self.Tasks[:]:
            if  self.total_ms <= task.TotalMS:
                task.Command.invoke()
                if task.CanDelete:
                    self.Tasks.remove(task)




def main():
    pass


if __name__ == "__main__":
    main()
