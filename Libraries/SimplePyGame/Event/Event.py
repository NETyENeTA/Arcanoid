import pygame as pg

from Event.EventType import EventType


class Event:
    class Types:
        EXECUTE_COMMAND = EventType.get_id()

    def __init__(self, type: int, dictionary: dict = None, **kwargs):
        # Если пришел словарь, используем его, иначе — пустой
        data = dictionary or {}
        # Добавляем в этот словарь всё, что пришло через kwargs
        data.update(kwargs)

        self.value = pg.event.Event(type, data)


def main():
    pass


if __name__ == "__main__":
    main()
