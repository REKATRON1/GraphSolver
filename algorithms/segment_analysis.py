import math
import heapq
import numpy as np

class LinAprx():
	def __init__(self, p1: tuple[float, float], p2: tuple[float, float]):
		if p2[0] != p1[0]:
			self.slope: float = (p2[1]-p1[1])/(p2[0]-p1[0])
			self.constant: float = p1[1]-p1[0]*self.slope
		else:
			self.slope: float = math.inf
			self.constant: float = p1[0]
	def get(self, x: float) -> float:
		return self.slope * x + self.constant
	def intersect(l1: object, l2: object) -> tuple[float, float]:
		if l1.slope == l2.slope:
			return math.inf, math.inf
		intersect_x = (l2.constant - l1.constant)/(l1.slope - l2.slope)
		intersect_y = l1.get(intersect_x)
		return intersect_x, intersect_y

def intersect_on_edge(e: tuple[tuple[float, float], tuple[float, float]], p: tuple[float, float]) -> bool:
	x, y = p
	return ((x >= min([e[0][0], e[1][0]]) and x <= max([e[0][0], e[1][0]]) and y > min([e[0][1], e[1][1]]) and y < max([e[0][1], e[1][1]])) or
			(x > min([e[0][0], e[1][0]]) and x < max([e[0][0], e[1][0]]) and y >= min([e[0][1], e[1][1]]) and y <= max([e[0][1], e[1][1]])))

def check_intersect(e1: tuple[tuple[float, float], tuple[float, float]], e2: tuple[tuple[float, float], tuple[float, float]]) -> bool:
	p11, p12 = e1
	p21, p22 = e2
	if p12[0] < p11[0]:
		p11, p12 = p12, p11
	if p22[0] < p21[0]:
		p21, p22 = p22, p21
	#p_1 always has smaller x-coord then p_2
	if p12[0] <= p21[0] or p11[0] >= p22[0] or (p11[0] == p12[0] and p21[0] == p22[0]) or (p11[1] == p21[1] and p12[1] == p22[1]):
		return False
	if p21[0] == p22[0]:
		p11, p12, p21, p22 = p21, p22, p11, p12
	if p11[0] == p12[0]:
		x = p11[0]
		prx_2 = LinAprx(p21, p22)
		return intersect_on_edge(e1, (x, prx_2.get(x))) and intersect_on_edge(e2, (x, prx_2.get(x)))
	else:
		prx_1 = LinAprx(p11, p12)
		prx_2 = LinAprx(p21, p22)
		if prx_1.slope == prx_2.slope:
			return prx_2.constant == prx_1.constant
		else:
			intersect_x, intersect_y = LinAprx.intersect(prx_1, prx_2)
		return intersect_on_edge(e1, (intersect_x, intersect_y)) and intersect_on_edge(e2, (intersect_x, intersect_y))

def breakup_edge_covers(path: list[tuple[float, float]]) -> tuple[list, list]:
	ani = []
	cm, max_breakups = 0, 1000
	overlaps = []
	start = True
	while cm < max_breakups and (start or len(overlaps) > 0):
		start = False
		cm += 1
		if len(overlaps) > 0:
			new_path = path.copy()
			start, end, typ = overlaps.pop(0)
			if typ < 2:
				#max_end > max_start
				#typ = index of bigger
				max_point = new_path.pop(start+typ)
				new_path.insert(end, max_point)
				
			else:
				#max_start >(=) max_end
				typ -= 2
				#typ = index of bigger
				max_point = new_path.pop(start+typ)
				new_path.insert(end+1, max_point)
			
			ani.append(((start, end), path, new_path))
			
			path = new_path
		
		overlaps = []
		edges = []
		for x in range(len(path)-1):
			p1, p2 = path[x], path[x+1]
			edges.append([p1,p2])
		for i, e1 in enumerate(edges):
			aprxi = LinAprx(e1[0], e1[1])
			for j, e2 in enumerate(edges):
				if i >= j or (i == 0 and j == len(edges) - 1):
					continue
				aprxj = LinAprx(e2[0], e2[1])
				if aprxi.slope == aprxj.slope and aprxi.constant == aprxj.constant:
					if aprxi.slope != math.inf:
						if min(e1[0][0], e1[1][0]) < max(e2[0][0], e2[1][0]) and max(e1[0][0], e1[1][0]) > min(e2[0][0], e2[1][0]) or (
							min(e1[0][0], e1[1][0]) == min(e2[0][0], e2[1][0]) or max(e1[0][0], e1[1][0]) == max(e2[0][0], e2[1][0])):
							if max(e1[0][0], e1[1][0]) < max(e2[0][0], e2[1][0]):
								overlaps.append((i,j,e1[0][0] < e1[1][0]))
							else:
								overlaps.append((i,j,2 + int(e2[0][0] < e2[1][0])))
					elif min(e1[0][1], e1[1][1]) < max(e2[0][1], e2[1][1]) and max(e1[0][1], e1[1][1]) > min(e2[0][1], e2[1][1]) or (
							min(e1[0][1], e1[1][1]) == min(e2[0][1], e2[1][1]) or max(e1[0][1], e1[1][1]) == max(e2[0][1], e2[1][1])):
						if max(e1[0][1], e1[1][1]) < max(e2[0][1], e2[1][1]):
							overlaps.append((i,j,e1[0][1] < e1[1][1]))
						else:
							overlaps.append((i,j,2 + int(e1[0][1] < e1[1][1])))
	return path, ani
	


def optimize_intersects(path: list[tuple[float, float]]) -> tuple[list, list]:
	path, ani = breakup_edge_covers(path)

	cm, max_swaps = 0, 1000
	intersections = []
	start = True
	while cm < max_swaps and (start or len(intersections) > 0):
		start = False
		cm += 1
		if len(intersections) > 0:
			start, end = 0, 0
			while len(intersections) > 0 and np.abs(start - end) < 2:
				start, end = intersections[0]
				intersections.pop(0)
			if np.abs(start - end) < 2:
				break
			start += 1
			end += 1
			new_path = path[:start]
			new_path.extend(path[start:end][::-1])
			new_path.extend(path[end:])
			ani.append(((start, end), path, new_path))
			path = new_path
		intersections = []
		edges = []
		for x in range(len(path)-1):
			p1, p2 = path[x], path[x+1]
			edges.append([p1,p2])
		for i, e1 in enumerate(edges):
			for j, e2 in enumerate(edges):
				if i >= j or (i == 0 and j == len(edges) - 1):
					continue
				if check_intersect(e1, e2):
					intersections.append((i,j))
	return path, ani

def get_angle(point_A: tuple[float, float], point_over: tuple[float, float], point_C: tuple[float, float]) -> float:
	if point_A != point_over and point_A != point_C and point_over != point_C:
		ba = np.array(point_A) - np.array(point_over)
		bc = np.array(point_C) - np.array(point_over)
		cos_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
		if cos_angle < -1:
			cos_angle = -0.9999
		elif cos_angle > 1:
			cos_angle = 0.9999
		angle = np.arccos(cos_angle)
		if np.isnan(angle) or np.isnan(np.degrees(angle)):
			print(point_A,point_over,point_C)
			print('cos', cos_angle)
			print('ang', angle)
			print('deg', np.degrees(angle))
		if angle == 0:
			angle = 0.0001
		return np.degrees(angle)
	return 0

def is_acute(point_A: tuple[float, float], point_over: tuple[float, float], point_C: tuple[float, float]) -> bool:
	return get_angle(point_A, point_over, point_C) < 90.0

def count_acute_angles(path: list[tuple[float, float]]) -> int:
	n: int = 0
	for x in range(2, len(path)):
		p1, p2, p3 = path[x-2], path[x-1], path[x]
		n += is_acute(p1, p2, p3)
	return n

def get_heap(points: list[tuple[float, float]], distance_matrix: list[list[float]], use_min: bool=True, mode: int=0) -> list[tuple[float, int, int]]:
	heap = []
	avg_distance, c = 0, 0
	spread: tuple[float, float, float, float] = math.inf, -math.inf, math.inf, -math.inf

	for x, p1 in enumerate(points):
		spread = min(spread[0], p1[0]), max(spread[1], p1[0]), min(spread[2], p1[1]), max(spread[3], p1[1])
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
	
	def coord_func(coord_idx: int, edge: tuple[tuple[float, float], tuple[float, float]], spread: tuple[float], 
						inverse: bool=False) -> float:
		p1, p2 = edge
		c1, c2 = p1[coord_idx], p2[coord_idx]
		mi, ma = spread[2*coord_idx], spread[2*coord_idx+1]
		offset = .1*max(np.abs(mi), np.abs(ma))
		mi -= offset
		ma += offset
		if c2 < c1:
			c1, c2 = c2, c1
		if inverse:
			return ((-c1 + ma)/(ma-mi))*((-c2 + ma)/(ma-mi))
		else:
			return ((c1 - mi)/(ma-mi))*((c2 - mi)/(ma-mi))

	avg_distance /= c
	for x, p1 in enumerate(points):
		for y, p2 in enumerate(points):
			if x >= y:
				continue
			d = distance_matrix[x,y]
			match mode:
				case 0 | 1 | 2:
					heapq.heappush(heap, (polyn_func(mode, d, avg_distance, not use_min), x, y))
				case 3 | 4:
					heapq.heappush(heap, (coord_func(mode-3, (p1,p2), spread, not use_min), x, y))

	return heap

def get_distance_matrix(points: list[tuple[float, float]], use_min: bool=True, use_func: int=0) -> list[list[float]]:
	distances = np.zeros((len(points), len(points)))
	
	for x, p1 in enumerate(points):
		for y, p2 in enumerate(points):
			if x >= y:
				continue
			d = distance(p1, p2)
			distances[x,y] = d
			distances[y,x] = d

	return distances

def total_length(edges: list[tuple[tuple[float, float], tuple[float, float]]]) -> float:
	if len(edges) == 0:
		return math.inf
	s: float = 0.0
	for edge in edges:
		p1, p2 = edge
		s += distance(p1, p2)
	return s

def path_length(points: list[tuple[float, float]]) -> float:
	if len(points) == 0:
		return math.inf
	s: float = 0.0
	for x in range(len(points)-1):
		p1, p2 = points[x], points[x+1]
		s += distance(p1, p2)
	return s

def distance(p1: tuple[float, float], p2: tuple[float, float]) -> float:
	return np.sqrt(sum([(x2-x1)**2 for x1, x2 in zip(p1, p2)]))