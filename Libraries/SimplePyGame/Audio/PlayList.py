
from os import path, listdir, getcwd
from random import shuffle

from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

class PlayList:


    def __init__(self, folder_path: str):
        # base_path = path.abspath(getcwd())

        # 2. Соединяем его с твоим относительным путем
        # Это превратит "../../../GameFiles/..." в реальный "C:/Users/.../GameFiles/..."
        # folder_path = path.normpath(path.join(base_path, folder_path))


        self.files = [path.join(folder_path, file) for file in listdir(folder_path) if file.endswith('.mp3')]
        self.queue = []

        self.shuffle()


    def shuffle(self):
        self.queue = self.files.copy()
        shuffle(self.queue)

    def next(self):
        if not self.queue:
            self.shuffle()

        current_track: str = self.queue.pop()

        audio = MP3(current_track, ID3=EasyID3)
        # duration = audio.info.length

        return current_track, audio



