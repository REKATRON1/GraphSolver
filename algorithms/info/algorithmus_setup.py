
from enum import Enum
from dataclasses import dataclass

from utility import Point

class SolvingMode(Enum):
    GraphSolve = 0
    PathSolve = 1

@dataclass
class AlgorithmusSetup():
    points: list[Point]
    solving_mode: SolvingMode