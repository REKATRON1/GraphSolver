
import math
from enum import Enum

from utility import Point
from algorithms.info import AlgoInfos, SolvingEval, Solution

class PathSolvingType(Enum):
    BruteForce = 0
    ClosestPtP = 1
    MultiPtP = 2
    Addbuild = 3

class PathSolvingExtra():
	def __init__(self, max_adj: int=math.inf):
		self.max_adj = max_adj

class AlgoInfosPathSolve(AlgoInfos):
    def __init__(self, solving_type: PathSolvingType, solving_extra: PathSolvingExtra, solving_eval: SolvingEval) -> None:
        match solving_type:
            case PathSolvingType.BruteForce:
                super().__init__(8)
            case PathSolvingType.ClosestPtP:
                super().__init__(175)
            case PathSolvingType.MultiPtP:
                super().__init__(175)
            case PathSolvingType.Addbuid:
                super().__init__(500)
    def get_solution(self, points: list[Point], solving_type: PathSolvingType) -> Solution:
        if len(points) > self.max_points:
            return Solution(message='Too many Points')
        #request soltion
    def set_solution(self, solution: Solution):
    	self.solution = solution