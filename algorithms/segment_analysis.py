import math
import heapq
import numpy as np

class LinAprx():
	def __init__(self, p1: tuple[float, float], p2: tuple[float, float]):
		if p2[0] != p1[0]:
			self.slope: float = (p2[1]-p1[1])/(p2[0]-p1[0])
			self.constant: float = p1[1]-p1[0]*self.slope
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
	if p12[0] <= p21[0] or p11[0] >= p22[0] or (p11[0] == p12[0] and p21[0] == p22[0]):
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
		intersect_x, intersect_y = LinAprx.intersect(prx_1, prx_2)
		return intersect_on_edge(e1, (intersect_x, intersect_y)) and intersect_on_edge(e2, (intersect_x, intersect_y))

def optimize_intersects(path: list[tuple[float, float]]) -> tuple[list, list]:
	ani = []
	cm, max_swaps = 0, 100
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

def func(func_idx: int, x: float, avg_x: float=0.0) -> float:
	match func_idx:
		case 0:
			return x
		case 1:
			return (x/avg_x)*(x/avg_x-2)
		case 2:
			return sum([f*(x**i) for i, f in enumerate([0, -2/avg_x, 5/(avg_x**2), -4/(avg_x**3), 1/(avg_x**4)])])
		case _:
			return 0.0


def get_distance_matrix(points: list[tuple[float, float]], use_min: bool=True, use_func: int=0) -> tuple[list[list[float]], list[tuple[float, int, int]]]:
	distances, heap = np.zeros((len(points), len(points))), []
	avg_distance, c = 0, 0
	for x, p1 in enumerate(points):
		for y, p2 in enumerate(points):
			if x >= y:
				continue
			d = distance(p1, p2)
			distances[x,y] = d
			distances[y,x] = d
			if use_func == 0:
				if use_min:
					heapq.heappush(heap, (func(use_func, d), x, y))
				else:
					heapq.heappush(heap, (-func(use_func, d), x, y))
			else:
				avg_distance += d
				c += 1
	if use_func == 0:
		return distances, heap
	avg_distance /= c
	for x, _ in enumerate(points):
		for y, _ in enumerate(points):
			if x >= y:
				continue
			d = distances[x,y]
			if use_min:
				heapq.heappush(heap, (func(use_func, d, avg_distance), x, y))
			else:
				heapq.heappush(heap, (-func(use_func, d, avg_distance), x, y))
	return distances, heap

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