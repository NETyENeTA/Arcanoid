from typing import Callable

import pygame as pg

from Event.CommandStuff.CommandManager import CommandManager
from Event.CommandStuff.Task import Task
from Event.Event import Event


class Command:
    _tasks: list[Task] = []

    class Default:
        LOOPS = 1
        MY_NAME = "command_object"

    def __init__(self, action: Callable | None, *args, action_name: str | None = None, delay: int | float = None,
                 ability_canceled_delete: bool = False, funcs_args: list = None, loops: int = Default.LOOPS,
                 **kwargs):

        self.action: Callable | None = action
        self.args = args
        self.func_args = funcs_args or []
        self.kwargs = kwargs

        self.loops: int = loops

        self.delay = delay
        self.__canceled = False
        self.CancelDelete = ability_canceled_delete

        self.__name: str = str(action_name or getattr(action, '__name__', action))

    @property
    def name(self):
        return self.__name

    def create(self, *args, action: Callable = None, delay: int | float = None,
               ability_canceled_delete: bool = False, funcs_args: list = None,
               **kwargs) -> 'Command':
        """Создает копию команды с новыми аргументами"""
        # Если args/kwargs не переданы, берем их из текущей команды
        _args = args if args else self.args
        _kwargs = kwargs if kwargs else self.kwargs
        _delay = delay if delay is not None else self.delay
        _action = action if action is not None else self.action
        _cancelDelete = ability_canceled_delete if ability_canceled_delete else self.CancelDelete
        _funcs_args = funcs_args if funcs_args else self.func_args

        # Возвращаем абсолютно новый объект
        return Command(_action, *_args, action_name=self.name,
                       delay=_delay, ability_canceled_delete=_cancelDelete, funcs_args=_funcs_args, **_kwargs)

    def invoke(self, manager: CommandManager | None = None,
               timeout: int | float = None, loops: int = None, locked: bool = False):
        """Регистрирует команду в менеджере (рекомендуемый способ)"""
        self.__canceled = locked
        wait_time = timeout if timeout is not None else self.delay
        loops = self.loops if loops is None else loops
        print(loops, self.__repr__())


        if wait_time is None or wait_time <= 0:
            self()
            return

        if not manager:
            self.sign_schedule(wait_time, loops, locked)
            return

        manager.add(self, wait_time, loops)

    def defer(self, timeout: float | int = None, loops: int = Default.LOOPS, locked: bool = False) -> None:
        """
        Old invoke with old system (pygame.time.set_timer, and pg.Event).
        :param timeout: Delay, if it's not null this overrides the self.delay.
        :param loops: How many times will it be repeated.
        :param locked: Should I block execution?
        :return: None, definitely
        """

        self.__canceled = locked
        wait_time = timeout if timeout is not None else self.delay
        loops = loops or self.loops

        if wait_time is None or wait_time <= 0:
            self()
            return

        event = Event(Event.Types.EXECUTE_COMMAND, {Command.Default.MY_NAME: self})

        pg.time.set_timer(event.value, int(wait_time * 1000), loops=loops)

    def sign_schedule(self, timeout: float | int = None, loops: int = None, locked: bool = False):
        self.schedule(self, timeout, self.loops if loops is None else loops, locked)

    @staticmethod
    def schedule(command: 'Command', timeout: float | int = None, loops: int = Default.LOOPS, locked: bool = False):
        """Статический метод для запуска, если нет доступа к экземпляру менеджера"""

        command.__canceled = locked
        wait_time = timeout if timeout is not None else command.delay
        if wait_time is None or wait_time <= 0:
            command()
            return

        task = Task(command, wait_time, loops)
        Command._tasks.append(task)

    @classmethod
    def update_schedule(cls):
        # print(cls._tasks)
        now = pg.time.get_ticks()
        for task in cls._tasks[:]:
            task.update(now)

            is_finished = getattr(task, 'is_finished', False)
            is_canceled = getattr(task.Command, 'is_canceled', False)
            cancel_delete = getattr(task.Command, 'CancelDelete', False)

            # Объединяем оба сценария удаления в одно понятное условие
            if is_finished or (is_canceled and cancel_delete):
                try:
                    cls._tasks.remove(task)
                except ValueError:
                    # Если сработал clear_tasks, игнорируем ошибку отсутствия задачи в списке
                    pass

    @property
    def is_canceled(self) -> bool:
        return self.__canceled

    def cancel(self):
        self.__canceled = True

    def resume(self):
        self.__canceled = False

    def __call__(self, *args, **kwargs):
        if self.action is None or self.__canceled:
            return None

        results = [func() for func in self.func_args]

        _args = [*self.args, *results, *args]
        _kwargs = {**kwargs, **self.kwargs}

        return self.action(*_args, **_kwargs)

    @classmethod
    def clear_tasks(cls):
        cls._tasks = []



    def __str__(self):
        return f'Action({self.name})'

    def __repr__(self):
        return (f'{self.__class__.__name__}(action=<name:{self.name}>, '
                f'args={self.args!r}, kwargs={self.kwargs!r})')

