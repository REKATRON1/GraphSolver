import pygame as pg
from ui.visualaddons import Sidebar, Bar
import extra.sidefunc as sf

def get_mouse_inputs(meta_infos, algo_infos, visual_infos) -> None:
	
	def check_buttons(meta_infos, algo_infos, visual_infos, bar, mouse_pos) -> bool:
		if isinstance(bar, Sidebar):
			for button_name, button_rect in bar.get_buttons(meta_infos, algo_infos):
				if button_rect.collidepoint(mouse_pos):
					return sf.switch_button(meta_infos, algo_infos, visual_infos, button_name)
		elif isinstance(bar, Bar):
			for button_name, button_rect in bar.get_buttons():
				if button_rect.collidepoint(mouse_pos):
					return sf.switch_button(meta_infos, algo_infos, visual_infos, button_name)
		return False

	if not any(pg.mouse.get_pressed(num_buttons=3)):
		visual_infos.mouse_pressed = False
	elif visual_infos.mouse_pressed:
		"""
		do nothing
		"""
	elif pg.mouse.get_pressed(num_buttons=3)[0]:
		visual_infos.mouse_pressed = True
		button_press = False
		button_press = check_buttons(meta_infos, algo_infos, visual_infos, visual_infos.right_sidebar, pg.mouse.get_pos())
		button_press |= check_buttons(meta_infos, algo_infos, visual_infos, visual_infos.left_sidebar, pg.mouse.get_pos())
		button_press |= check_buttons(meta_infos, algo_infos, visual_infos, visual_infos.bottom_bar, pg.mouse.get_pos())
		
		if meta_infos.active_status == 0 and not button_press and pg.mouse.get_pos()[0] < visual_infos.right_sidebar.left_edge_x:
			place_point(meta_infos, algo_infos, visual_infos, pg.mouse.get_pos())
	elif pg.mouse.get_pressed(num_buttons=3)[2]:
		visual_infos.mouse_pressed = True
		if len(algo_infos.points) > 0:
			algo_infos.points.pop(-1)
		else:
			algo_infos.solution = None
	
from data import example_data as tda
from data.example_data import tc

def get_key_inputs(key_infos, meta_infos, algo_infos, visual_infos) -> None:
	#'Space' -> spawn random point
	if meta_infos.active_status == 0 and key_infos[pg.K_SPACE]:
		place_point(meta_infos, algo_infos, visual_infos)
	#'Up' -> spawn 25 random points
	if meta_infos.active_status == 0 and key_infos[pg.K_UP]:
		for _ in range(25):
			place_point(meta_infos, algo_infos, visual_infos)
	#'Down' -> delete 25 points
	if meta_infos.active_status == 0 and key_infos[pg.K_DOWN]:
		for _ in range(25):
			if len(algo_infos.points) > 0:
				algo_infos.points.pop(-1)
			else:
				algo_infos.solution = None
	#'Enter' -> enters solving-mode
	if meta_infos.active_mode != 2 and key_infos[pg.K_RETURN]:
		if meta_infos.active_status != 1:
			algo_infos.get_solution(meta_infos, visual_infos)
		else:
			meta_infos.active_status = 0
	#'Delete' -> clears solved path
	if meta_infos.active_status == 0 and key_infos[pg.K_DELETE]:
		algo_infos.solution.solved_path = []
	#'F11' -> swaps between fullscreen
	if key_infos[pg.K_F11]:
		meta_infos.fullscreen = not meta_infos.fullscreen
		if meta_infos.fullscreen:
			main_screen = pg.display.set_mode((0,0), pg.FULLSCREEN)
		else:
			main_screen = pg.display.set_mode((1280, 720), pg.RESIZABLE)
			if algo_infos.solution != None:
				algo_infos.solution.solved_path = []
			algo_infos.points, meta_infos.active_status = [], 0
	#DEBUG! 'D' -> printout points
	if key_infos[pg.K_d]:
		print(algo_infos.points)
	if meta_infos.active_status != 1 and key_infos[pg.K_l]:
		if meta_infos.active_status != 2:
			meta_infos.active_status = 2
		else:
			meta_infos.active_status = 0
	if meta_infos.active_mode == 0 and meta_infos.active_status != 1 and key_infos[pg.K_e]:
		if meta_infos.active_status != 3:
			meta_infos.active_status = 3
		else:
			meta_infos.active_status = 0

import random
def place_point(meta_infos, algo_infos, visual_infos, position=None) -> None:
	"""
	places a point on the screen if the maximum amount of points is not reached
	"""
	if len(algo_infos.points) >= algo_infos.max_points:
		return
	if position == None:
		position = random.randint(0, int(visual_infos.right_sidebar.left_edge_x)), random.randint(0, meta_infos.screen_size[1])
	if algo_infos.scaling != 1:
		algo_infos.scaling = 1
	algo_infos.points.append(position)