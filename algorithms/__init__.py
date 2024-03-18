
from typing import TypeAlias

from .info import AlgorithmusSetup, SolvingMode
from .info import SolutionInfo, SolutionVisualInfo

from .visualize_solution import draw_solution

from .graph_solving import RawSolvingEval, SolvingEval, GraphSolvingType, GraphSolvingExtra, AlgorithmusSetupGraphSolve
#from .path_solving import PathSolvingType, PathSolvingExtra

from .run import request_solution

SolvingType: TypeAlias = GraphSolvingType# | PathSolvingType
SolvingExtra: TypeAlias = GraphSolvingExtra# | PathSolvingExtra