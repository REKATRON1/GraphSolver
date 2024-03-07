import numpy as np
from algorithms import segment_analysis as sga
import math
from numpy.random import choice as np_choice
import random

class Colony():
	def __init__(self, points):
		self.points = points
		self.weights = np.ones((len(points), len(points)))
		self.distance_grid = sga.get_distance_matrix(points)
	def run(self, generations, generation_size):
		all_bests = []
		best_score, best_path = math.inf, []
		for x in range(generations):
			self.weights, new_best_path = self.run_generation(self.weights, generation_size)
			new_best_path_score = self.get_path_score(new_best_path)
			if new_best_path_score < best_score:
				best_score, best_path = new_best_path_score, new_best_path
			all_bests.append(best_path)
			print(f'Gen num: {x}')
		return all_bests
	def run_generation(self, prev_weights, generation_size):
		generation_paths = []
		best_score, best_path = math.inf, []
		for x in range(generation_size):
			new_path = self.get_new_path(prev_weights)
			#print(new_path)
			new_path_score = self.get_path_score(new_path)
			if new_path_score < best_score:
				best_score, best_path = new_path_score, new_path
			#print(f'path num: {x}')
			generation_paths.append(new_path)
		new_weights = self.adapt_weights(prev_weights, generation_paths)
		return new_weights, best_path
	def get_new_path(self, weights):
		path = [random.randint(0, len(self.points)-1)]
		prev = path[0]
		visited_points = set()
		visited_points.add(prev)
		while len(visited_points) < len(self.points):
			next_point = self.get_next_point(weights, prev, visited_points)
			visited_points.add(next_point)
			path.append(next_point)
			prev = next_point
		return [self.points[x] for x in path]
	def get_next_point(self, weights, start, visited_points):
		p_weights = Colony.get_p_weights(weights[start], visited_points)# [weights[start][x] if (2**x)^mask > mask else 0 for x in range(len(weights[start]))]
		normalized_weights = [x/sum(p_weights) for x in p_weights]
		n = np_choice(range(len(self.points)), 1, p=normalized_weights)[0]
		return n
	def get_p_weights(weights, visited_points):
		n_weights = [0 if x in visited_points else weights[x] for x in range(len(weights))]
		if sum(n_weights) == 0:
			return Colony.get_p_weights([p+1 for p in weights])
		return n_weights
	def get_path_score(self, path):
		return (sga.count_acute_angles(path) + 1) * sga.path_length(path)
	def adapt_weights(self, weights, generation_paths):
		paths_plus_score = [(self.get_path_score(x), x) for x in generation_paths]
		#print(paths_plus_score)
		sorted_paths = sorted(paths_plus_score, key=lambda x: x[0])
		best_score = sorted_paths[0][0]
		for sc, path in enumerate(sorted_paths):
			path_rel_score = best_score/sc
			for x in range(len(path)-2):
				s, e = path[x], path[x+1]
				weights[s,e] += path_rel_score
		return weights

def solve_graph(points, generations, tour=False, angles_threshold_to_avoid=0):
	main_colony = Colony(points)
	all_bests = main_colony.run(generations, 25)
	return all_bests[-1], all_bests