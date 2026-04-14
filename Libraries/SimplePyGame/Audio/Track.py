from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from pygame import mixer


class Track:

    def __init__(self, path = ""):
        self.path = path
        self.audio = MP3(path, ID3=EasyID3) if path else None
        mixer.music.set_volume(0.5)

    @property
    def name(self) -> str:
        return self.info("title", "Annonimous")[0]

    def info(self, key: str, default):
        if self.audio:
            return self.audio.get(key, [default])
        return default

    def update(self, path):
        self.__init__(path)

    def restart(self):
        self.load()
        self.play()

    def load(self):
        self.loads(self.path)

    @staticmethod
    def loads(path: str):
        mixer.music.load(path)

    @staticmethod
    def play() -> None:
        mixer.music.play()
        # pass

    @property
    def busy(self) -> bool:
        return mixer.music.get_busy()

    @property
    def duration(self) -> float:
        if self.audio:
            return self.audio.info.length

        return 0.0

    @property
    def current_pos(self) -> int:
        return mixer.music.get_pos()

    @property
    def current_second(self) -> float:
        return self.current_pos / 1000

    @property
    def progress(self) -> int | float:
        if not self.busy or self.duration == 0:
            return 0
        return min(self.current_second / self.duration, 1)
