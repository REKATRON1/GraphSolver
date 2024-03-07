import pygame as pg
from ui import visualaddons
import time

from extra import sidefunc as sf
from algorithms import path_finder
from algorithms import graph_solver

class MetaInfos():
	def __init__(self):
		"""
		base pygame stats
		"""
		self.screen_size: tuple[int, int] = (1280, 720)
		self.screen_center: tuple[int, int] = (self.screen_size[0]/2, self.screen_size[1]/2)
		self.fullscreen: bool = False
		self.main_font = None
		"""
		meta variables
		"""
		self.tick_rate: float = 500.0
		self.delta_time: float = 0.0

		#0: graph_solve, #1: path_solve
		self.active_mode: int = 0

		#0: default, 1: solving, 2: loading, 3: extra
		self.active_status: int = 0

		self.all_buttons_converter: list[list[str] | list[list[str]]] = [['Min Graph','Pathsolving','NaN'],
										[['Addbuid'],
										['Animate', 'Looping']],
										[['Brute Force', 'Closest PtP', 'Multi cPtP', 'Addbuid'],
										['Enable Tour', 'Intersect Optim.', 'No Acute Angles'],
										['Animate', 'Looping']],
										[[]],
									['Keep Relations', 'Include Scal.'],
									['Use Min', 'Use Max', 'Default', 'Shifted Parabola', 'Double Parabola', 'X', 'Y'],
									['Solve']]
		self.all_buttons_activity: list[list[bool]] = [[False for x in l] for l in self.get_all_buttons()]
		self.switch_button('Min Graph')
		self.switch_button('Addbuid')
		self.switch_button('Use Min')
		self.switch_button('Default')

		"""
		runtime variables
		"""
		self.running: bool = True

		self.warned: list[bool] = [False]
		self.error_end: float = 0.0
		self.error_message: str = ''

	def switch_active_mode(self, new_mode: int) -> None:
		if self.active_mode != new_mode:
			self.active_mode = new_mode
			self.all_buttons_activity = [[False for x in l] for l in self.get_all_buttons()]
			self.all_buttons_activity[0][self.active_mode] = True
			match self.active_mode:
				case 0:
					self.all_buttons_activity[1][0] = True
					self.switch_button('Use Min')
					self.switch_button('Default')
				case 1:
					self.all_buttons_activity[1][1] = True
					self.switch_button('Use Min')
					self.switch_button('Default')
			if self.active_status == 3:
				self.active_status = 0

	def get_button_activity(self, b: str) -> bool:
		for btidx, bt in enumerate(self.get_all_buttons()):
			for bnidx, bn in enumerate(bt):
				if b == bn:
					try:
						return self.all_buttons_activity[btidx][bnidx]
					except IndexError:
						return False
		return False

	def switch_button(self, b: str) -> None:
		for btidx, bt in enumerate(self.get_all_buttons()):
			for bnidx, bn in enumerate(bt):
				if b == bn:
					if btidx == 0 and self.all_buttons_activity[btidx][bnidx]:
						self.switch_active_mode(self.get_all_buttons()[0].index(b))
						return
					self.all_buttons_activity[btidx][bnidx] = not self.all_buttons_activity[btidx][bnidx]

	def get_all_buttons(self) -> list[list[str]]:
		buttons = self.all_buttons_converter[:1]
		match self.active_mode:
			case 0:
				buttons.extend(self.all_buttons_converter[1])
			case 1:
				buttons.extend(self.all_buttons_converter[2])
			case 2:
				buttons.extend(self.all_buttons_converter[3])
		buttons.extend(self.all_buttons_converter[-3:])
		return buttons

class AlgoInfos():
	def __init__(self):
		"""
		algorithm variables
		"""
		self.max_points: int = 500
		self.points: list[tuple[int, int]] = []
		self.solving_type: int = 1
		self.scaling: float = 1.0
		
		"""
		runtime variables
		"""
		self.solution = None
	
	def get_solution(self, meta_infos, visual_infos) -> None:
		try:
			self.solving_type = meta_infos.all_buttons_activity[1].index(True)
		except:
			print(meta_infos.all_buttons_activity)
		if meta_infos.active_mode == 1:
			if self.solving_type == 0 and (not meta_infos.warned[0] and len(self.points) > 7):
				#waring bcs. the brute force algorithim cant handle many points -> prevents accident crashes
				meta_infos.error_end, meta_infos.error_message = pg.time.get_ticks()+4000, "Running the BF-Algorithm with >7 points can cause serious lags!"
				meta_infos.warned[0] = True
				return
			elif self.solving_type == 0 and len(self.points) > 10:
				meta_infos.error_end, meta_infos.error_message = pg.time.get_ticks()+4000, "Can not run the BF-Algorithm with >10 points!"
				return
			elif self.solving_type in [1,2] and len(self.points) > 200:
				meta_infos.error_end, meta_infos.error_message = pg.time.get_ticks()+4000, "Can not run the PtP-Algorithms with >200 points!"
				return
		start_time = time.perf_counter()
		meta_infos.active_status = 1
		extras = {meta_infos.get_all_buttons()[2][i]:True for i, x in enumerate(meta_infos.all_buttons_activity[2]) if x}
		if meta_infos.active_mode != 2:
			for k in {meta_infos.get_all_buttons()[-2][i]:True for i, x in enumerate(meta_infos.all_buttons_activity[-2]) if x}:
				if k in meta_infos.get_all_buttons()[-2][2:]:
					extras['Func idx'] = meta_infos.get_all_buttons()[-2][2:].index(k)
				else:
					extras[k] = True
		
		self.solution = Solution.request(self.points, meta_infos.active_mode, self.solving_type, extras)
		visual_infos.animation_status = 0
		visual_infos.c_animation_phase = 0
		visual_infos.n_animation_phase = 1 + meta_infos.get_button_activity('Intersect Optim.')
		end_time = time.perf_counter()
		meta_infos.error_end, meta_infos.error_message = pg.time.get_ticks()+4000, f"Finished after {sf.convert_time(end_time-start_time)}"

class Solution():
	def __init__(self, solved_path, animation_path, extra_animation_path, length, num_angles=0):
		self.solved_path = solved_path
		self.animation_path = animation_path
		self.extra_animation_path = extra_animation_path
		self.length, self.num_angles = length, num_angles

	def request(points: list[tuple[int, int]], active_mode: int, solving_type: int, extras_enables: dict[str, bool]) -> object: #returns Solution object
		match active_mode:
			case 0:
				return graph_solver.find_subgraph(points, mode=solving_type, use_min=extras_enables.get('Use Min', False), use_func=extras_enables.get('Func idx', 0))
			case 1:
				return path_finder.find_path_in_graph(points, mode=solving_type, tour=extras_enables.get('Enable Tour', False), 
					intersection_check=extras_enables.get('Intersect Optim.', False), avoid_acute_angles=extras_enables.get('No Acute Angles', False),
					use_func=extras_enables.get('Func idx', 0), use_min=extras_enables.get('Use Min', False))

class VisualInfos():
	def __init__(self, meta_infos):
		"""
		visualizing stats
		"""
		self.point_size: int = 4
		self.animation_speed: int = 10000
		#Buttons
		self.sidebar_button_size: tuple[int, int] = (150, 40)

		self.animation_status: int = 0
		self.n_animation_phase: int = 1
		self.c_animation_phase: int = 0

		#Sidebars
		self.right_sidebar = visualaddons.Sidebar(meta_infos.screen_size[0]-self.sidebar_button_size[0]-.4*self.sidebar_button_size[1], meta_infos.screen_size[0], [], [], self.sidebar_button_size[1])
		self.left_sidebar = visualaddons.Sidebar(0, self.sidebar_button_size[0]+.4*self.sidebar_button_size[1], [], [], self.sidebar_button_size[1])
		
		self.bottom_bar = visualaddons.Bar(['Min Graph','Pathsolving','NaN'], None, None, size=40, 
												alignment_mode=2, draw_separation=True)

		"""
		input variables
		"""
		self.mouse_pressed: bool = False
	
	def update_window_sizes(self, main_screen, meta_infos) -> None:
		"""
		test for window-resizing
		"""
		meta_infos.screen_size = (main_screen.get_width(), main_screen.get_height())
		meta_infos.screen_center = (meta_infos.screen_size[0]/2, meta_infos.screen_size[1]/2)

		self.right_sidebar.left_edge_x = main_screen.get_width()-self.sidebar_button_size[0]-.4*self.sidebar_button_size[1]
		self.right_sidebar.right_edge_x = main_screen.get_width()
		self.left_sidebar.right_edge_x = self.sidebar_button_size[0]+.4*self.sidebar_button_size[1]
		self.bottom_bar.top_left_corner = 0, 0
		self.bottom_bar.max_bottom_right_corner = main_screen.get_width(), min(main_screen.get_height(), self.bottom_bar.size*len(self.bottom_bar.texts))
