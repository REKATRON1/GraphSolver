

def interpolate(x: float, y: float, c: float) -> float:
    return (1-c)*x + c*y

def interpolate_tuple(t1: tuple, t2: tuple, c: float) -> tuple:
    return tuple([interpolate(x,y,c) for x,y in zip(t1, t2)])


def clamp(x: float, mi: float, ma: float) -> float:
    return min(ma, max(x, mi))