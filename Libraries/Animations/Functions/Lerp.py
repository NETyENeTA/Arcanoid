def lerp(start: float, end: float, t: float) -> float:
    """
    Линейная интерполяция между start и end.
    t — коэффициент от 0.0 до 1.0 (процент сближения).
    """
    return start + (end - start) * t


def lerp_safe_tuple(start: tuple | list, end: tuple | list, t: tuple | list | float | int) -> tuple:
    # Безопасная распаковка с заполнением нулями, если данных не хватает
    x1, y1 = (list(start) + [0, 0])[:2]
    x2, y2 = (list(end) + [0, 0])[:2]

    t1, t2 = (list(t) + [0, 0])[:2] if isinstance(t, (tuple, list)) else (t, t)

    # Для t такая же логика или твой вариант с проверкой типа
    # if isinstance(t, (tuple, list)):
    #     t1, t2 = (list(t) + [0, 0])[:2]
    # else:
    #     t1 = t2 = t

    return lerp(x1, x2, t1), lerp(y1, y2, t2)


def lerp_tuple(start: tuple | list, end: tuple | list, t: tuple | list | float | int) -> tuple:
    x1, y1 = start[:2]
    x2, y2 = end[:2]
    t1, t2 = t[:2] if isinstance(t, (tuple, list)) else (t, t)

    return lerp(x1, x2, t1), lerp(y1, y2, t2)


def lerp_dict(start: dict, end: dict, t: dict) -> dict:
    _start = (start.get('x', 0), start.get('y', 0))
    _end = (end.get('x', 0), end.get('y', 0))
    _t = (t.get('x', 0), t.get('y', 0))

    result = lerp_tuple(_start, _end, _t)
    return {"x": result[0], "y": result[1], "t": t}
