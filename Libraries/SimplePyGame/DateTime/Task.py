from Event.CommandStuff.Command import Command


class Task:
    def __init__(self, seconds: int, command: Command, can_delete: bool = False):

        self.TotalMS = seconds * 1000
        self.Command = command

        self.CanDelete = can_delete




def main():
    pass


if __name__ == "__main__":
    main()
