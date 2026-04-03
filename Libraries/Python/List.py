


def get_at(collection: list | tuple, index, default=None):
    try:
        return collection[index]
    except IndexError:
        return default