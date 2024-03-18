

from algorithms import AlgorithmusSetup, SolvingMode, SolvingType
from algorithms import SolutionInfo
from utility import Point

class AlgorithmusData():
    def __init__(self, algorithmus_setup: AlgorithmusSetup) -> None:
        self.algorithmus_setup: AlgorithmusSetup = algorithmus_setup
        self.solution: SolutionInfo = None
    def set_algorithmus_setup(self, new_algo_setup: AlgorithmusSetup) -> None:
        self.algorithmus_setup = new_algo_setup
    def change_points(self, new_points: list[Point]) -> None:
        self.algorithmus_setup.points = new_points
    def change_solving_mode(self, new_mode: SolvingMode) -> None:
        self.algorithmus_setup.solving_mode = new_mode
    def change_solving_type(self, new_type: SolvingType) -> None:
        try:
            self.algorithmus_setup.solving_type = new_type
        except:
            print('error in runtime stats/algorithmus data/change solving type!')
    def set_solution(self, new_solution: SolutionInfo) -> None:
        self.solution = new_solution