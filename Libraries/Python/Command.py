from typing import Callable


class Command:

    def __init__(self, action: Callable, *args, action_name: str | None = None, **kwargs):
        self.action: Callable = action
        self.args = args
        self.kwargs = kwargs
        self.__name: str = str(action_name or getattr(action, '__name__', action))

    @property
    def name(self):
        return self.__name

    def __call__(self, *args, **kwargs):

        _args = [*self.args, *args]
        _kwargs = {**kwargs, **self.kwargs}

        return self.action(*_args, **_kwargs)


    def __str__(self):
        return f'Action({self.name})'

    def __repr__(self):
        return (f'{self.__class__.__name__}(action=<name:{self.name}>, '
                f'args={self.args!r}, kwargs={self.kwargs!r})')

