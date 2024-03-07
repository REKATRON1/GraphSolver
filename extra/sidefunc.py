import numpy as np

def interpolate_on_line(p1: tuple[int, int], p2: tuple[int, int], c: float) -> tuple[int, int]:
	return tuple(interpolate_list(list(p1), list(p2), c))

def interpolate_list(l1: list[float], l2: list[float], c: float) -> list[float]:
	return [interpolate(x1, x2, c) for x1, x2 in zip(l1, l2)]

def interpolate(a: float, b: float, p: float) -> float:
	return (1-p)*a + p*b

def convert_time(t: float) -> str:
	postfix: list[str] = ['s', 'ms', 'µs', 'ns']
	i: int = 0
	while t < 10 and i + 1 < len(postfix):
		t *= 1000
		i += 1
	return f'{int(np.round(t))}{postfix[i]}'

from data import example_data as tda
from data.example_data import tc
def switch_button(meta_infos, algo_infos, visual_infos, button_name: str) -> bool:
	exact_one_lists: list[list[str]] = [['Min Graph','Pathsolving','NaN'], 
						['Brute Force', 'Closest PtP', 'Multi cPtP', 'Addbuid'],
						['Use Min', 'Use Max'], ['Default', 'Shifted Parabola', 'Double Parabola']]
	distinct_lists: list[list[str]] = [['Addbuid', 'No Acute Angles'], ['Intersect Optim.', 'No Acute Angles']]
	dependent_lists: list[list[str]] = [['Animate', 'Looping'], ['Keep Relations', 'Include Scal.']]

	meta_infos.switch_button(button_name)
	for exact_one_list in exact_one_lists:
		if not button_name in exact_one_list:
			continue
		if sum([meta_infos.get_button_activity(x) for x in exact_one_list]) != 1:
			for x in exact_one_list:
				if meta_infos.get_button_activity(x):
					meta_infos.switch_button(x)
			meta_infos.switch_button(button_name)

	for distinct_list in distinct_lists:
		if not button_name in distinct_list:
			continue
		if sum([meta_infos.get_button_activity(x) for x in distinct_list]) > 1:
			for x in distinct_list:
				if x != button_name and meta_infos.get_button_activity(x):
					meta_infos.switch_button(x)

	for dependent_list in dependent_lists:
		if not button_name in dependent_list:
			continue
		if not meta_infos.get_button_activity(dependent_list[0]) and any([meta_infos.get_button_activity(x) for x in dependent_list[1:]]):
			for x in dependent_list:
				if meta_infos.get_button_activity(x):
					meta_infos.switch_button(x)
	
	match button_name:
		case 'Min Graph' | 'Pathsolving' | 'NaN':
			if algo_infos.solution != None:
				algo_infos.solution.solved_path = []
		case 'Solve':
			if meta_infos.active_status != 1:
				algo_infos.get_solution(meta_infos, visual_infos)
			else:
				meta_infos.active_status = 0
		case 'Clear':
			algo_infos.points = []
			algo_infos.solution = None
		case 'No Acute Angles':
			if sum([meta_infos.get_button_activity(x) for x in ['Brute Force', 'Closest PtP', 'Multi cPtP', 'Addbuid']]) == 0:
				meta_infos.switch_button('Closest PtP')
		case '':
			return False
		case _:
			match button_name.split():
				case 'Load', i if i.isdigit():
					algo_infos.solution = None
					algo_infos.points, algo_infos.scaling = tda.normalize_data((visual_infos.right_sidebar.left_edge_x, meta_infos.screen_size[1]), tc[int(i)], keep_relations=meta_infos.get_button_activity('Keep Relations'))
					meta_infos.active_status = 0
	return True