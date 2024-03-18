
import heapq

from utility import Point, iVector2, GraphAnalysis

def addbuild(points: list[Point], max_adj: int, eval: int, inverse: bool, fac_dst: bool, extra: int=0) -> list[iVector2]:
	edges: List[iVector2] = []
	distance_matrix: list[list[float]] = GraphAnalysis.get_distance_matrix(points)
	distance_heap = GraphAnalysis.get_heap(points, distance_matrix, eval, inverse, fac_dst, extra)
	adjacency_count: list[list[int]] = [[] for _ in points]
	subgraph_marker: dict[int, int] = {}
	max_maker: int = 0
	
	def change_subgraph(prev: int , new: int) -> None:
		for idx, v in subgraph_marker.items():
			if v == prev:
				subgraph_marker[idx] = new
	for _ in range(len(points)-1):
		added = False
		while not added:
			next_distance = heapq.heappop(distance_heap)
			_, ip1, ip2 = next_distance
			if subgraph_marker.get(ip1) == None or subgraph_marker.get(ip2) == None or subgraph_marker.get(ip1) != subgraph_marker.get(ip2):
				if len(adjacency_count[ip1]) < max_adj and len(adjacency_count[ip2]) < max_adj:
					edges.append((ip1, ip2))
					added = True
					adjacency_count[ip1].append(ip2)
					adjacency_count[ip2].append(ip1)
					if subgraph_marker.get(ip1) == None and subgraph_marker.get(ip2) == None:
						max_maker += 1
						subgraph_marker[ip1], subgraph_marker[ip2] = max_maker, max_maker
					elif subgraph_marker.get(ip1) == None:
						subgraph_marker[ip1] = subgraph_marker.get(ip2)
					elif subgraph_marker.get(ip2) == None:
						subgraph_marker[ip2] = subgraph_marker.get(ip1)
					else:
						change_subgraph(subgraph_marker[ip2], subgraph_marker[ip1])
	return edges