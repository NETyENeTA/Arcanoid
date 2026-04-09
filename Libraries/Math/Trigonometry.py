from math import sin


class Sinus:

    @staticmethod
    def positive(value: float) -> float:
        return abs(sin(value))

    @staticmethod
    def negative(value: float) -> float:
        return -abs(sin(value))

    @staticmethod
    def smooth_01(value: float) -> float:
        return (sin(value) + 1) / 2


def main():
    pass


if __name__ == "__main__":
    main()
