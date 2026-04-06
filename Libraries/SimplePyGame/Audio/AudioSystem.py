from Libraries.SimplePyGame.Audio.PlayList import PlayList
from Libraries.SimplePyGame.Audio.Track import Track, mixer


class AudioSystem:

    def __init__(self):
        mixer.init()
        self.Player = PlayList("../GameFiles/Media/audio/music")
        self.CurrentTrack: Track | None = None

    @property
    def volume(self):
        return mixer.music.get_volume()

    @volume.setter
    def volume(self, value):
        mixer.music.set_volume(max(0.0, min(1.0, value)))


    def play_next(self):
        track_path, audio_data = self.Player.next()
        self.CurrentTrack = Track(track_path, audio_data)
        self.CurrentTrack.load()
        self.CurrentTrack.play()

    def update(self):
        if not self.is_busy:
            self.play_next()

    @property
    def is_busy(self):
        return mixer.music.get_busy()