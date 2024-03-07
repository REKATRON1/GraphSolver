import numpy as np
import math
import heapq
from algorithms import segment_analysis as sga
from algorithms import aco
from extra import datacompression

def find_path_in_graph(points: list[tuple[int, int]], mode: int=1, tour: bool=False, 
						intersection_check: bool=False, avoid_acute_angles: bool=False,
						use_func: int=0, use_min: bool=True) -> object:
	if avoid_acute_angles:
		angles_threshold_to_avoid: float = 90.0
	else:
		angles_threshold_to_avoid: float = 0.0
	if len(points) <= 1:
		return datacompression.Solution(solved_path=[], animation_path=[], extra_animation_path=[], length=0)
	sol, ani, extra = [], [], []
	match mode:
		case 0:
			sol = solve_graph_bf(points, tour, angles_threshold_to_avoid)
		case 1:
			sol = solve_graph_ptp(points, tour, angles_threshold_to_avoid)
		case 2:
			sol = solve_graph_mptp(points, tour, angles_threshold_to_avoid)
		case 3:
			sol, ani = solve_graph_addb(points, tour, angles_threshold_to_avoid, use_func, use_min)
		case 4:
			sol, ani = aco.solve_graph(points, 100, tour, angles_threshold_to_avoid)

	if intersection_check:
		if len(ani) == 0:
			ani = sol
		sol, extra = sga.optimize_intersects(sol)

	if len(ani) == 0 and len(sol) != 0:
		ani = sol
	if avoid_acute_angles:
		return datacompression.Solution(solved_path=sol, animation_path=ani, extra_animation_path=[extra], length=sga.path_length(sol), num_angles=sga.count_acute_angles(sol))
	return datacompression.Solution(solved_path=sol, animation_path=ani, extra_animation_path=[extra], length=sga.path_length(sol))

def solve_graph_bf(points, tour, angles_threshold_to_avoid):
	return solve_graph_bf_int(points, 0, [], tour, angles_threshold_to_avoid)

def solve_graph_bf_int(points, mask, cpath, tour, angles_threshold_to_avoid):
	if mask == 2**len(points)-1:
		if tour:
			cpath.append(cpath[0])
		return cpath
	best_len, best_path = math.inf, []
	for x in range(2):
		if x and (len(best_path) > 0 or len(cpath) < 2):
			break
		for i, n in enumerate([2**x for x in range(len(points))]):
			if n^mask > mask:
				if not x and len(cpath) > 1 and angles_threshold_to_avoid > 0:
					if sga.get_angle(cpath[-2], cpath[-1], points[i]) <= angles_threshold_to_avoid:
						continue
				n_cpath = cpath.copy()
				n_cpath.append(points[i])
				n_path = solve_graph_bf_int(points, mask^n, n_cpath, tour, angles_threshold_to_avoid)
				n_len = sga.path_length(n_path)
				if n_len < best_len:
					best_len, best_path = n_len, n_path
	return best_path

def solve_graph_ptp(points, tour, angles_threshold_to_avoid):
	best_score, best_path = math.inf, []
	for i, p in enumerate(points):
		n_path = solve_graph_ptp_int(points, [points[i]], 2**i, angles_threshold_to_avoid)
		if tour:
			n_path.append(points[i])
		n_len = sga.path_length(n_path)
		if angles_threshold_to_avoid == 0:
			score = n_len
		else:
			n_ang = sga.count_acute_angles(n_path)
			score = n_len * (n_ang + 1)
		if score < best_score:
			best_score, best_path = score, n_path
	return best_path

def solve_graph_ptp_int(points, prev, mask, angles_threshold_to_avoid):
	if mask == 2**len(points)-1:
		return [prev[-1]]
	best_score, best_score_idx = math.inf, -1
	for x in range(2):
		if x and (best_score_idx >= 0 or len(prev) < 2):
			break
		for i, n in enumerate([2**x for x in range(len(points))]):
			if n^mask > mask:
				dst = sga.distance(prev[-1], points[i])
				if not x and len(prev) > 1 and angles_threshold_to_avoid > 0:
					ang = sga.get_angle(prev[-2], prev[-1], points[i])
					if ang <= angles_threshold_to_avoid:
						score = dst*(30*max(10,np.abs(ang-180))/(angles_threshold_to_avoid))
					else:
						score = dst*(3*max(10,np.abs(ang-180))/(angles_threshold_to_avoid))
				else:
					score = dst
				if score < best_score:
					best_score, best_score_idx = score, i
	cpath = [prev[-1]]
	rec_path = solve_graph_ptp_int(points, [prev[-1], points[best_score_idx]], mask + 2**best_score_idx, angles_threshold_to_avoid)
	cpath.extend(rec_path)
	return cpath

def solve_graph_mptp(points, tour, angles_threshold_to_avoid):
	best_score, best_path = math.inf, []
	for i, p in enumerate(points):
		#if i != 26:
		#	continue
		#print(f'Start: {points[i]}')
		n_path, r = solve_graph_mptp_int(points, [points[i]], [points[i]], 2**i, angles_threshold_to_avoid)
		n_path.append(points[i])
		n_path.extend(r)
		if tour:
			n_path.append(n_path[0])
		n_len = sga.path_length(n_path)
		if angles_threshold_to_avoid == 0:
			score = n_len
		else:
			n_ang = sga.count_acute_angles(n_path)
			score = n_len * (n_ang + 1)
		if score < best_score:
			best_score, best_path = score, n_path
	return best_path

def solve_graph_mptp_int(points, prev1, prev2, mask, angles_threshold_to_avoid):
	if mask == 2**len(points)-1 or (len(prev1) == 0 and len(prev2) == 0):
		return [], []
	p1b1_score, p1bi1 = math.inf, -1
	p1b2_score, p1bi2 = math.inf, -1
	p2b1_score, p2bi1 = math.inf, -1
	p2b2_score, p2bi2 = math.inf, -1
	for x in range(2):
		if x and (p1bi2 >= 0 or len(prev1) < 2) and (p2bi2 >= 0 or len(prev2) < 2):
			break
		for i, n in enumerate([2**x for x in range(len(points))]):
			if n^mask > mask:
				dst1 = sga.distance(prev1[-1], points[i])
				if not x and len(prev1) > 1 and angles_threshold_to_avoid > 0:
					ang1 = sga.get_angle(prev1[-2], prev1[-1], points[i])
					if ang1 <= angles_threshold_to_avoid:
						score1 = dst1*(30*max(10,np.abs(ang1-180))/(angles_threshold_to_avoid))
					else:
						score1 = dst1*(3*max(10,np.abs(ang1-180))/(angles_threshold_to_avoid))
				else:
					score1 = dst1
				if score1 < p1b1_score:
					p1b2_score, p1bi2 = p1b1_score, p1bi1
					p1b1_score, p1bi1 = score1, i
				elif score1 < p1b2_score and i != p1bi1:
					p1b2_score, p1bi2 = score1, i

				dst2 = sga.distance(prev2[-1], points[i])
				if not x and len(prev2) > 1 and angles_threshold_to_avoid > 0:
					ang2 = sga.get_angle(prev2[-2], prev2[-1], points[i])
					if ang2 <= angles_threshold_to_avoid:
						score2 = dst2*(30*max(10,np.abs(ang2-180))/(angles_threshold_to_avoid))
					else:
						score2 = dst2*(3*max(10,np.abs(ang2-180))/(angles_threshold_to_avoid))
				else:
					score2 = dst2
				if score2 < p2b1_score:
					p2b2_score, p2bi2 = p2b1_score, p2bi1
					p2b1_score, p2bi1 = score2, i
				elif score2 < p2b2_score and i != p2bi1:
					p2b2_score, p2bi2 = score2, i
	nl_prev, nr_prev = -1, -1
	if p1bi1 != p2bi1:
		nl_prev, nr_prev = p1bi1, p2bi1
	elif p1b1_score <= p2b1_score:
		nl_prev = p1bi1
		if p2bi2 >= 0 and p2bi2 != p1bi1:
			nr_prev = p2bi2
	else:
		if p1bi2 >= 0 and p1bi2 != p2bi1:
			nl_prev = p1bi2
		nr_prev = p2bi1
	n_prev1 = []
	if len(prev1) > 0:
		n_prev1.append(prev1[-1])
	mask_add = 0
	if nl_prev >= 0:
		n_prev1.append(points[nl_prev])
		mask_add += 2**nl_prev
	n_prev2 = []
	if len(prev2) > 0:
		n_prev2.append(prev2[-1])
	if nr_prev >= 0:
		n_prev2.append(points[nr_prev])
		mask_add += 2**nr_prev
	left, right = solve_graph_mptp_int(points, n_prev1, n_prev2, mask + mask_add, angles_threshold_to_avoid)
	if len(n_prev2) > 1:
		cright = [n_prev2[-1]]
		cright.extend(right)
	else:
		cright = right
	if len(n_prev1) > 1:
		left.append(n_prev1[-1])
	return left, cright

def solve_graph_addb(points: list[tuple[float, float]], tour, angles_threshold_to_avoid, mode: int=0, use_min: bool=True):
	edges = []
	distance_matrix = sga.get_distance_matrix(points)
	distance_heap = sga.get_heap(points, distance_matrix, use_min, mode)
	adjacency_count = [[] for _ in points]
	subgraph_marker = {}
	max_maker = 0
	
	def change_subgraph(prev, new):
		for idx, v in subgraph_marker.items():
			if v == prev:
				subgraph_marker[idx] = new

	while True:
		#NO Tour differentiating!!!!
		if (len(points) <= 1 or (all(adjacency_count) and sum([len(x) for x in adjacency_count]) >= 2*len(points) - 2)):
			break
		added = False
		while not added:
			next_distance = heapq.heappop(distance_heap)
			_, ip1, ip2 = next_distance
			if subgraph_marker.get(ip1) == None or subgraph_marker.get(ip2) == None or subgraph_marker.get(ip1) != subgraph_marker.get(ip2):
				if len(adjacency_count[ip1]) < 2 and len(adjacency_count[ip2]) < 2:
					edges.append((points[ip1], points[ip2]))
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
	path = []
	cidx = [len(x) for x in adjacency_count].index(1)
	path = [points[cidx]]
	while len(adjacency_count[cidx]) > 0:
		nidx = adjacency_count[cidx][0]
		adjacency_count[cidx].pop(0)
		adjacency_count[nidx].remove(cidx)
		cidx = nidx
		path.append(points[nidx])
	if tour:
		path.append(path[0])
	return path, edges

def deepcopy(l):
	if type(l) == list:
		n_l = []
		for x in l:
			n_l.append(deepcopy(x))
		return n_l
	else:
		return l