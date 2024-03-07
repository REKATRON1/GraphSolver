import numpy as np
import math
import heapq
from algorithms import segment_analysis as sga
from algorithms import aco
from extra import datacompression

def find_subgraph(points: list[tuple[int, int]], mode: int=0, use_min: bool=True, use_func: int=0) -> object:
	match mode:
		case 0:
			sol = solve_graph_addb(points, use_min, use_func)
	return datacompression.Solution(solved_path=sol, animation_path=sol, extra_animation_path=[], length=sga.total_length(sol))

def solve_graph_addb(points: list[tuple[int, int]], use_min: bool=True, mode: int=0):
	edges = []
	distance_matrix = sga.get_distance_matrix(points)
	edge_heap = sga.get_heap(points, distance_matrix, use_min, mode)
	subgraph_marker = {}
	max_maker = 0
	
	def change_subgraph(prev, new):
		for idx, v in subgraph_marker.items():
			if v == prev:
				subgraph_marker[idx] = new

	for _ in range(len(points)-1):
		added = False
		while not added and len(edge_heap) > 0:
			next_distance = heapq.heappop(edge_heap)
			_, ip1, ip2 = next_distance
			if subgraph_marker.get(ip1) == None or subgraph_marker.get(ip2) == None or subgraph_marker.get(ip1) != subgraph_marker.get(ip2):
				edges.append((points[ip1], points[ip2]))
				added = True
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