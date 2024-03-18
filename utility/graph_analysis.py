import numpy as np
import heapq

import math
from typing import TypeAlias, TypeVar, Generic

from utility import Point, iVector2, Vector2, Vector3

V = TypeVar('V', Vector2, Vector3)
class GraphAnalysis(Generic[V]):
    def length(v1: V):
        return np.linalg.norm(v1) 
    def difference(v1: V, v2: V):
        return np.array(v2) - np.array(v1)
    def distance(p1: Point, p2: Point):
        return GraphAnalysis.length(GraphAnalysis.difference(p2,p1))
    def get_distance_matrix(points: list[Point]):
        distance_matrix = np.zeros((len(points), len(points)))
        for x, p1 in enumerate(points):
            for y, p2 in enumerate(points):
                if x >= y:
                    continue
                distance = GraphAnalysis.distance(p1, p2)
                distance_matrix[x,y] = distance
                distance_matrix[y,x] = distance
        return distance_matrix
    def get_heap(points: list[Point], distance_matrix: list[list[float]], mode=0, inverse: bool=True, 
				fac_dst: bool=False, extra: int=0) -> list[tuple[float, int, int]]:
        from algorithms import RawSolvingEval
        if len(points) == 0:
            return []
        heap = []
        avg_distance, c = 0, 0
        spread: list[tuple[float, float]] = [(math.inf, -math.inf) for _ in points[0]]

        for x, p1 in enumerate(points):
            spread = [(min(spread[x][0], p1[x]), max(spread[x][1], p1[x])) for x in range(len(p1))]
            for y, p2 in enumerate(points):
                if x >= y:
                    continue
                avg_distance += distance_matrix[x,y]
                c += 1
        
        def polyn_func(func_idx: int, x: float, avg_x: float=0.0, inverse: bool=False) -> float:
            ret = 0
            match func_idx:
                case 0:
                    ret = x
                case 1:
                    ret = (x/avg_x)*(x/avg_x-2)
                case 2:
                    ret = sum([f*(x**i) for i, f in enumerate([0, -2/avg_x, 5/(avg_x**2), -4/(avg_x**3), 1/(avg_x**4)])])
            if inverse:
                return -ret
            else:
                return ret
        
        def coord_func(points: list[Point], dst_mx: list[list[float]], coord_idx: int, edge: iVector2, spread: tuple[float, float, float, float], 
                            inverse: bool=False, fac_dst: bool=False) -> float:
            p1, p2 = points[edge[0]], points[edge[1]]
            c1, c2 = p1[coord_idx], p2[coord_idx]
            mi, ma = spread[coord_idx][0], spread[coord_idx][1]
            offset = .1*max(np.abs(mi), np.abs(ma))
            mi -= offset
            ma += offset
            if c2 < c1:
                c1, c2 = c2, c1
            if fac_dst:
                d = dst_mx[edge]
            else:
                d = 1
            if inverse:
                return ((-c1 + ma)/(ma-mi))*((-c2 + ma)/(ma-mi))*d
            else:
                return ((c1 - mi)/(ma-mi))*((c2 - mi)/(ma-mi))*d
        avg_distance /= c
        for x, p1 in enumerate(points):
            for y, p2 in enumerate(points):
                if x >= y:
                    continue
                d = distance_matrix[x,y]
                match mode:
                    case RawSolvingEval.mindst:
                        heapq.heappush(heap, (polyn_func(0, d, avg_distance, inverse), x, y))
                    case RawSolvingEval.avgdst:
                        heapq.heappush(heap, (polyn_func(1, d, avg_distance, inverse), x, y))
                    case RawSolvingEval.dparab:
                        heapq.heappush(heap, (polyn_func(2, d, avg_distance, inverse), x, y))
                    case RawSolvingEval.coord:
                        heapq.heappush(heap, (coord_func(points, distance_matrix, extra, (x,y), spread, inverse, fac_dst), x, y))

        return heap