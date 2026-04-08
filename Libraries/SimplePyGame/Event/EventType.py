from pygame import USEREVENT


class EventType:
    __last_User_Event_ID = USEREVENT

    @classmethod
    def get_id(cls):
        """
        Get Custom the event type of the current Event
        :return: int, type of the event
        """
        cls.__last_User_Event_ID += 1
        return cls.__last_User_Event_ID


def main():
    pass


if __name__ == "__main__":
    main()
