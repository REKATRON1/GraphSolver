
import math
from typing import TypeAlias
from enum import Enum
from dataclasses import dataclass

from utility import Point
from algorithms.info import AlgorithmusSetup

class RawSolvingEval(Enum):
	mindst = 0
	avgdst = 1
	dparab = 2
	coord = 3

@dataclass
class SolvingEval:
	eval_type: RawSolvingEval = RawSolvingEval.mindst
	extra: int = 0
	inverse: bool = False
	fac_dst: bool = False

class GraphSolvingType(Enum):
    Addbuild = 0

@dataclass
class GraphSolvingExtra():
    max_points: int
    max_adj: int=math.inf
    solving_eval: SolvingEval=SolvingEval(0)

@dataclass
class AlgorithmusSetupGraphSolve(AlgorithmusSetup):
    solving_type: GraphSolvingType
    solving_extra: GraphSolvingExtra