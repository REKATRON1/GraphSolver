
from runtime_stats import AlgorithmusData
from algorithms import AlgorithmusSetupGraphSolve, GraphSolvingExtra, SolvingEval, RawSolvingEval

def get_main_algo_setup() -> AlgorithmusData:
    return AlgorithmusData(AlgorithmusSetupGraphSolve([], 0, 0, 
        GraphSolvingExtra(500, max_adj=2, solving_eval=SolvingEval(RawSolvingEval.mindst, extra=0))))