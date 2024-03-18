

from utility import Point, iVector2


class SolutionInfo():
    def __init__(self, points: list[Point]=None, solution: list[iVector2]=None, time: float=0, length: float=0, extra: list[float]=None, message: str='') -> None:
        if message:
            self.message: str = message
        else:
            self.points: list[Point] = points
            self.solution: list[iVector2] = solution
            self.time: float = time
            self.length: float = length
            self.extra: list[float] = extra
    def has_solution(self) -> bool:
        return not self.message

class SolutionVisualInfo():
    def __init__(self, points: list[Point], solution_steps: list[iVector2]) -> None:
        self.points: list[Point] = points
        self.solition_steps: list[int] | list[iVector2] = solution_steps