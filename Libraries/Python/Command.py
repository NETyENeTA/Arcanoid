from typing import Callable

import pygame as pg

from Event.Event import Event


class Command:
    class Default:
        LOOPS = 1
        MY_NAME = "command_object"

    def __init__(self, action: Callable | None, *args, action_name: str | None = None, delay: int | float = None,
                 **kwargs):

        self.action: Callable | None = action
        self.args = args
        self.kwargs = kwargs

        self.delay = delay
        self.__canceled = False

        self.__name: str = str(action_name or getattr(action, '__name__', action))

    @property
    def name(self):
        return self.__name

    def invoke(self, timeout: float | int = None, loops: int = Default.LOOPS, locked: bool = False) -> None:

        self.__canceled = locked
        wait_time = timeout if timeout is not None else self.delay

        if wait_time is None or wait_time <= 0:
            self()
            return

        event = Event(Event.Types.EXECUTE_COMMAND, {Command.Default.MY_NAME: self})

        pg.time.set_timer(event.value, int(wait_time * 1000), loops=loops)

    def cancel(self):
        self.__canceled = True

    def resume(self):
        self.__canceled = False

    def __call__(self, *args, **kwargs):
        if self.action is None or self.__canceled:
            return None

        _args = [*self.args, *args]
        _kwargs = {**kwargs, **self.kwargs}

        return self.action(*_args, **_kwargs)


    def __str__(self):
        return f'Action({self.name})'

    def __repr__(self):
        return (f'{self.__class__.__name__}(action=<name:{self.name}>, '
                f'args={self.args!r}, kwargs={self.kwargs!r})')

