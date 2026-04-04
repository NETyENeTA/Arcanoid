import pygame as pg
from pygame._sdl2 import Renderer, Texture

from Libraries.SimplePyGame.SDL2.Text.Font import Font
from Libraries.SimplePyGame.SDL2.Text.CashedFonts import CashedFonts as Cashe

class FontSystem:
    def __init__(self, renderer: Renderer):
        self.__Fonts = []
        self.__cache = Cashe()
        self.__renderer = renderer  # Теперь работаем с рендерером
        pg.font.init()

    def add(self, name, path, size, filename=None):
        self.__Fonts.append(Font(name, path, size, filename))

    def get_font(self, name: str, size: int = None) -> pg.font.Font:
        font_info = next((f for f in self.__Fonts if f.name == name), None)

        if not font_info:
            print(f"Font '{name}' not found in FontSystem.")
            sys_path = pg.font.match_font(name)
            return self.__cache.get_font(sys_path, size if size else 24)

        target_size = size if size is not None else font_info.size
        return self.__cache.get_font(font_info.full_path, target_size)


    def get_surface(self, text: str, name: str, size: int = None,
                  color=(255, 255, 255), bg_color=None, padding=5,):

        font = self.get_font(name, size)

        surf = font.render(text, True, color)

        return surf

    def get_texture(self, text: str, name: str, size: int = None,
                  color=(255, 255, 255)):

        surf = self.get_surface(text, name, size, color)

        texture = Texture.from_surface(self.__renderer, surf)

        return texture


    def get_with_bg_texture(self, text: str, name: str, size: int = None,
                         color=(255, 255, 255), bg_color=(0, 0, 0), padx=10, pady=5) -> Texture:
        """Создает и возвращает одну текстуру с текстом на цветном фоне"""

        font = self.get_font(name, size)

        # 1. Рендерим сам текст
        text_surf = font.render(text, True, color)

        # 2. Создаем новую пустую Surface нужного размера (с учетом отступов)
        w = text_surf.get_width() + padx * 2
        h = text_surf.get_height() + pady * 2
        final_surf = pg.Surface((w, h), pg.SRCALPHA)  # SRCALPHA для прозрачности, если нужно

        # 3. Заливаем фон
        final_surf.fill(bg_color)

        # 4. Накладываем текст поверх фона в центр
        final_surf.blit(text_surf, (padx, pady))

        # 5. Превращаем всё это в одну SDL2 Текстуру
        return Texture.from_surface(self.__renderer, final_surf)

    def draw_with_bg(self, text: str, name: str, size: int = None,
                  color=(255, 255, 255), bg_color=None, padding=5, pos=(0, 0)):

        font = self.get_font(name, size)
        surf = font.render(text, True, color)

        rect = pg.Rect(pos, (surf.get_width() + padding * 2, surf.get_height() + padding * 2))

        if bg_color:
            self.__renderer.draw_color = bg_color
            self.__renderer.fill_rect(rect)


        texture = Texture.from_surface(self.__renderer, surf)

        text_pos = (pos[0] + padding, pos[1] + padding)
        texture.draw(dstrect=pg.Rect(text_pos, surf.get_size()))



    def draw_text(self, text: str, name: str, size: int = None,
                  color=(255, 255, 255), pos=(0, 0)):

        if len(text) == 0:
            return

        texture = self.get_texture(text, name, size, color)
        w, h = texture.get_rect().size

        # surf = self.get_surface(text, name, size, color)
        # texture = Texture.from_surface(self.__renderer, surf)


        texture.draw(dstrect=pg.Rect(pos[0], pos[1], w, h))
        # texture.draw(dstrect=pg.Rect(pos[0], pos[1], surf.get_width(), surf.get_height()))


    def get_texture_drew_text(self, text, name, size = None, color=(255, 255, 255)) -> Texture | None:

        if len(text) == 0:
            return None

        texture = self.get_texture(text, name, size, color)

        return texture

