
from Libraries.SimplePyGame.Text.Font import Font, pg
from Libraries.SimplePyGame.Text.CashedFonts import CashedFonts as Cashe
from Libraries.SimplePyGame.Positions import Vec2
from Libraries.SimplePyGame.Colors import Colors, Color


class FontSystem:
    def __init__(self, default_screen: pg.Surface):
        self.__Fonts = []
        self.__cache = Cashe()
        self.__default_screen = default_screen
        pg.font.init()

    def add(self, name, path, size):
        # Добавляем инфо о шрифте в список
        self.__Fonts.append(Font(name, path, size))

    def get_font(self, name: str, size: int = None) -> pg.font.Font:
        # 1. Ищем инфо о шрифте
        font_info = next((f for f in self.__Fonts if f.name == name), None)

        if not font_info:
            # Если имя вообще не зарегистрировано, пробуем найти в системе
            # или отдаем дефолт, чтобы игра не упала
            print(f"Warning: Font '{name}' not registered. Trying system match...")
            sys_path = pg.font.match_font(name)  # Пытаемся найти системный по этому имени

            if sys_path:
                target_size = size if size is not None else 24
                return self.__cache.get_font(sys_path, target_size)
            else:
                return pg.font.Font(None, size if size else 24)

        # 2. Если инфо есть, пробуем достать из кэша
        target_size = size if size is not None else font_info.size

        try:
            return self.__cache.get_font(font_info.full_path, target_size)
        except Exception:
            # Если файл из font_info вдруг удалили, ищем системную замену (Arial/Sans)
            fallback_path = pg.font.match_font("arial") or pg.font.match_font("sans")
            return self.__cache.get_font(fallback_path, target_size)


    def draw_text(self, text: str, name: str, size: int = None,
                  color: Color = Colors.BLACK, pos: Vec2 = None,
                  screen: pg.Surface | None = None):
        """Утилита для быстрой отрисовки текста одной строкой"""

        # 1. Защита от изменяемого аргумента по умолчанию
        position = pos.xy if pos else (0, 0)

        # 2. Получаем шрифт
        font = self.get_font(name, size)

        # 3. Рендерим (используем .full или .rgba из твоего класса Color)
        surf = font.render(text, True, color.full)

        # 4. Определяем целевую поверхность
        target_surface = screen if screen else self.__default_screen

        # 5. Рисуем
        target_surface.blit(surf, position)

    def clear(self):
        self.__Fonts.clear()
        self.__cache.clear()

