def lerp(start: float, end: float, t: float) -> float:
    """
    Линейная интерполяция между start и end.
    t — коэффициент от 0.0 до 1.0 (процент сближения).
    """
    return start + (end - start) * t


def lerp_tuple(start: float, end: float, t: float) -> tuple:
    ...