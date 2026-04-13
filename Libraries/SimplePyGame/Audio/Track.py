from mutagen.mp3 import MP3
from pygame import mixer


class Track:

    def __init__(self, path, audio: MP3):
        self.path = path
        self.audio = audio
        mixer.music.set_volume(0.5)

    @property
    def name(self) -> str:
        return self.info("title", "Annonimous")[0]

    def info(self, key: str, default):
        return self.audio.get(key, [default])

    def load(self):
        mixer.music.load(self.path)

    @property
    def duration(self):
        return self.audio.info.length

    @staticmethod
    def play():
        mixer.music.play()
        # pass

    @property
    def busy(self):
        return mixer.music.get_busy()

    @property
    def current_pos(self):
        return mixer.music.get_pos()

    @property
    def current_second(self):
        return self.current_pos / 1000

    @property
    def progress(self) -> int | float:
        if not self.busy or self.duration == 0:
            return 0
        return min(self.current_second / self.duration, 1)
