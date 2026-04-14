from typing import Callable

from Event.CommandStuff.Command import Command
from Libraries.SimplePyGame.Audio.PlayList import PlayList
from Libraries.SimplePyGame.Audio.Track import Track, mixer


class AudioSystem:

    def __init__(self):
        mixer.init()
        self.Player = PlayList("../GameFiles/Media/audio/music")
        self.CurrentTrack: Track = Track()
        self.events: list[Command] = []

    def sign_event(self, event):
        self.events.append(event)

    @property
    def progress(self) -> float:
        if self.CurrentTrack.audio:
            return self.CurrentTrack.progress

        return 0.00

    @property
    def percentage(self) -> float:
        if self.CurrentTrack.audio:
            return self.CurrentTrack.progress * 100

        return 0.00

    @property
    def volume(self):
        return mixer.music.get_volume()

    @volume.setter
    def volume(self, value):
        mixer.music.set_volume(max(0.0, min(1.0, value)))

    def play_next(self):
        self.play(self.Player.next)

    def play_prev(self):
        self.play(self.Player.prev)


    def play(self, method: Callable):
        if not self.Player.queue:
            return

        path = method()

        self.CurrentTrack.update(path)
        self.CurrentTrack.restart()

        self.invoke_events()

    def invoke_events(self):
        for event in self.events:
            event.invoke()

    def update(self):
        if not self.is_busy:
            self.play_next()

    @property
    def is_busy(self):
        return mixer.music.get_busy()
