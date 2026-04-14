
from os import path, listdir, getcwd
from random import shuffle

class PlayList:
    def __init__(self, folder_path: str):
        self.files = [path.join(folder_path, file) for file in listdir(folder_path) if file.endswith('.mp3')]
        self.queue = []
        self.currentIndex = -1 # Начинаем с -1, чтобы первый next() сделал индекс 0
        self.shuffle()

    def shuffle(self):
        self.queue = self.files.copy()
        shuffle(self.queue)
        self.currentIndex = -1

    def __getitem__(self, index:int):
        current_track = self.queue[index]
        return current_track

    def next(self):
        if not self.queue:
            return ""

        # Увеличиваем индекс и зацикливаем, если дошли до конца
        self.currentIndex = (self.currentIndex + 1) % len(self.queue)
        return self[self.currentIndex]

    def prev(self):
        if not self.queue:
            return ""

        # Уменьшаем индекс. В Python -1 % len(queue) автоматически вернет последний индекс
        self.currentIndex = (self.currentIndex - 1) % len(self.queue)
        return self[self.currentIndex]



def main():
    pass


if __name__ == "__main__":
    main()
