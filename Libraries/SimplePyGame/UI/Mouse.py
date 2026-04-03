import pygame as pg

from Libraries.SimplePyGame.Positions import Vec2

from typing import Literal


class Mouse:


    @staticmethod
    def toggle_cursor_visibility() -> None:
        pg.mouse.set_visible(not pg.mouse.get_visible())

    @staticmethod
    def set_cursor_visibility(visible: bool) -> None:
        pg.mouse.set_visible(visible)


    @staticmethod
    def pressed(buttons: Literal[3, 5] = 3):
        return pg.mouse.get_pressed(buttons)

    @staticmethod
    def pos() -> Vec2:
        return Vec2(pg.mouse.get_pos())

