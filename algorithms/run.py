
from .info import AlgorithmusSetup, SolutionInfo, SolvingMode

def request_solution(algorithmus_setup: AlgorithmusSetup) -> SolutionInfo:
    match algorithmus_setup.solving_mode:
        case 0:
            from .graph_solving import request_solution as run
            return run(algorithmus_setup)