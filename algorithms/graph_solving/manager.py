
import math
from time import perf_counter

from algorithms.info import SolutionInfo
from .graph_solving_infos import AlgorithmusSetupGraphSolve
from .addbuild import addbuild

def request_solution(algo_info: AlgorithmusSetupGraphSolve) -> SolutionInfo:
    start_time = perf_counter()
    match algo_info.solving_type:
        case 0:
            graph_edges_idx = addbuild(points=algo_info.points, max_adj=algo_info.solving_extra.max_adj, 
                                        eval=algo_info.solving_extra.solving_eval.eval_type, 
                                        inverse=algo_info.solving_extra.solving_eval.inverse, 
                                        fac_dst=algo_info.solving_extra.solving_eval.fac_dst,
                                        extra=algo_info.solving_extra.solving_eval.extra)
            return SolutionInfo(points=algo_info.points, solution=graph_edges_idx, time=perf_counter()-start_time)
    return SolutionInfo(message='No matching GraphSolvingAlgoithm found')