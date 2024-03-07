import pygame as pg
import numpy as np
import math

from extra import sidefunc as sf
from data.example_data import tc

def draw_screen(main_screen, meta_infos, algo_infos, visual_infos) -> None:
	"""
	draws the right sidebar with infos regarding the type of algorithm used
	"""
	"""
	display of a potential error message at the top of the screen
	"""
	if len(meta_infos.error_message) > 0 and pg.time.get_ticks() < meta_infos.error_end + 1000:
		if pg.time.get_ticks() < meta_infos.error_end:
			text_surface = meta_infos.main_font.render(meta_infos.error_message, False, "white")
			text_rect = text_surface.get_rect(center=(meta_infos.screen_center[0], .5*visual_infos.sidebar_button_size[1]))
			main_screen.blit(text_surface, text_rect)
		else:
			#Fade out
			x: int = int(np.round(((meta_infos.error_end + 1000 - pg.time.get_ticks())/1000*255)))
			text_surface = meta_infos.main_font.render(meta_infos.error_message, False, pg.Color(x,x,x))
			text_rect = text_surface.get_rect(center=(meta_infos.screen_center[0], .5*visual_infos.sidebar_button_size[1]))
			main_screen.blit(text_surface, text_rect)

	if meta_infos.active_status != 1:
		"""
		display bottom bar
		"""
		visual_infos.bottom_bar.draw(main_screen, meta_infos)


	"""
	display of the right sidebar
	"""
	visual_infos.right_sidebar.top_texts = [f"Points: {len(algo_infos.points)}"]
	visual_infos.right_sidebar.fixed_bottom_texts = [meta_infos.get_all_buttons()[-1][0], f'FPS: {np.round(1/max(0.0001, meta_infos.delta_time), 1)}']
	
	match meta_infos.active_mode:
		case 0 | 1:
			if meta_infos.active_status == 1:
				sol_len: float = np.round(algo_infos.solution.length, 1)
				if meta_infos.get_button_activity('Include Scal.'):
					sol_len: float = np.round(sol_len/algo_infos.scaling,2)
				visual_infos.right_sidebar.top_texts.append(f'Path len: {sol_len}')
				if meta_infos.get_button_activity('No Acute Angles'):
					visual_infos.right_sidebar.top_texts.append(f'Acute ang: {algo_infos.solution.num_angles}')
			else:
				visual_infos.right_sidebar.fixed_bottom_texts.insert(1, 'Clear')

			for button_type, active_state_type in list(zip(meta_infos.get_all_buttons(), meta_infos.all_buttons_activity))[1:-3]:
				visual_infos.right_sidebar.top_texts.append('')
				for button_name, button_active in zip(button_type, active_state_type):
					if not button_name == 'Looping' or meta_infos.get_button_activity('Animate'):
						if button_active:
							visual_infos.right_sidebar.top_texts.append(button_name)
						elif meta_infos.active_status != 1:
							visual_infos.right_sidebar.top_texts.append(button_name)
			
			solve_button = visual_infos.right_sidebar.get_buttons(meta_infos, algo_infos)[-1][1]
			if meta_infos.active_status == 1:
				#diplay color to green if 'in solving mode'
				pg.draw.rect(main_screen, "green", solve_button)
			else:
				pg.draw.rect(main_screen, pg.Color(80, 175, 80), solve_button)

			visual_infos.right_sidebar.draw(main_screen, meta_infos)
		
	"""
	draw left sidebar
	"""
	if meta_infos.active_status == 2:
		visual_infos.left_sidebar.fixed_bottom_texts = ['','Keep Relations']
		if meta_infos.get_button_activity('Keep Relations'):
			visual_infos.left_sidebar.fixed_bottom_texts.append('Include Scal.')
		visual_infos.left_sidebar.top_texts = []
		for i, txt in enumerate(tc):
			visual_infos.left_sidebar.top_texts.append(f'Load {i}')

		visual_infos.left_sidebar.draw(main_screen, meta_infos)
	elif meta_infos.active_status == 3:
		"""
		options for weighting?
		"""
		visual_infos.left_sidebar.fixed_bottom_texts = []
		visual_infos.left_sidebar.top_texts = meta_infos.get_all_buttons()[-2][:2]
		visual_infos.left_sidebar.top_texts.append('')
		visual_infos.left_sidebar.top_texts.extend(meta_infos.get_all_buttons()[-2][2:])
		visual_infos.left_sidebar.draw(main_screen, meta_infos)
		
def draw_solution(main_screen, meta_infos, algo_infos, visual_infos) -> None:
	if len(algo_infos.points) > 0 and algo_infos.solution != None:
		if meta_infos.active_status != 1 or not meta_infos.get_button_activity('Animate'):
			match meta_infos.active_mode:
				case 0:
					for edge in algo_infos.solution.solved_path:
						p1, p2 = edge
						pg.draw.line(main_screen, "green", p1, p2)
				case 1:
					for x in range(len(algo_infos.solution.solved_path)-1):
						p1, p2 = algo_infos.solution.solved_path[x], algo_infos.solution.solved_path[x+1]
						pg.draw.line(main_screen, "green", p1, p2)
		elif meta_infos.active_status == 1:
			#calculate animation status
			dt: float = min(50/1000, meta_infos.delta_time)
			if meta_infos.get_button_activity('Looping'):
				#looping behaviour
				if visual_infos.animation_status + dt*1000 >= visual_infos.animation_speed:
					visual_infos.c_animation_phase = visual_infos.c_animation_phase + 1
				if visual_infos.c_animation_phase >= visual_infos.n_animation_phase:
					visual_infos.c_animation_phase = 0
				visual_infos.animation_status = (visual_infos.animation_status + dt*1000) % visual_infos.animation_speed
			else:
				#if not looping: exit active_status when animation finished
				visual_infos.animation_status = min(visual_infos.animation_speed, (visual_infos.animation_status + dt*1000))
				if visual_infos.animation_status == visual_infos.animation_speed:
					visual_infos.animation_status = 0
					visual_infos.c_animation_phase += 1
				if visual_infos.c_animation_phase >= visual_infos.n_animation_phase:
					meta_infos.active_status = 0
					visual_infos.c_animation_phase = 0
			#animation-process
			if len(algo_infos.solution.solved_path) > 0 and len(algo_infos.solution.animation_path) > 0 and animate_solution(main_screen, meta_infos, algo_infos, visual_infos):
				visual_infos.c_animation_phase += 1
				if meta_infos.get_button_activity('Looping'):
					if visual_infos.c_animation_phase >= visual_infos.n_animation_phase:
						visual_infos.c_animation_phase = 0
				else:
					if visual_infos.c_animation_phase >= visual_infos.n_animation_phase:
						meta_infos.active_status = 0
						visual_infos.c_animation_phase = 0

def animate_solution(main_screen, meta_infos, algo_infos, visual_infos) -> bool:	
	"""
	animates found solution based on the type of solving algorithm used
	animations are split into multiple phases depending on the solving algorithms used
	"""
	if visual_infos.c_animation_phase == 0:
		"""
		default animation phase:
		showing just a portion of the solution relative to the animation_status based of the passed time
		"""
		if meta_infos.active_mode == 1 and algo_infos.solving_type in [0, 1]:
			"""
			Default solving algorithm
			animation works by splitting the total animation duration in one portion per edge in solution
			and showing just the first n edges where n*duration_per_edge < animation_status
			the remaining status (over the whole multiple of duration_per_edge) is converted into a partial
			display of the n+1 edge.
			"""
			animation_percent: float = visual_infos.animation_status/visual_infos.animation_speed
			#calculate the amount of edges fully visible in animation
			n: int = int((len(algo_infos.solution.animation_path))*animation_percent)
			
			#display of the first n edges:
			for x in range(n):
				p1, p2 = algo_infos.solution.animation_path[x], algo_infos.solution.animation_path[x+1]
				pg.draw.line(main_screen, "green", p1, p2)
				#calculate the duration per edge in the animation
			duration_per_edge: int = int(visual_infos.animation_speed/(len(algo_infos.solution.animation_path)))
				#draw the next edge in the solution partially based on the animation_status
			if len(algo_infos.solution.animation_path) > n+1:
				pn1, pn2 = algo_infos.solution.animation_path[n], algo_infos.solution.animation_path[n+1]
				#calculate the displayed percent of the next edge
				line_percent: float = (visual_infos.animation_status % duration_per_edge)/duration_per_edge
				#interpolate the end point of the displayed edge between the actual start and end points of the next edge based on the line_percent
				np2: tuple[int, int] = sf.interpolate_on_line(pn1, pn2, line_percent)
				pg.draw.line(main_screen, "green", pn1, np2)
		elif meta_infos.active_mode == 1 and algo_infos.solving_type == 2:
			"""
			multi point-to-point solving algorithm
			animation works by finding the central point of the solution and
			animating the 'default animation' in both directions of the solution
			"""
			animation_percent: float = visual_infos.animation_status/visual_infos.animation_speed
			#finding the middle of the solution
			mid: int = int(len(algo_infos.solution.animation_path)/2) #int(n/2) => bcs if even num points, last step should be left step (exmp.: 1->0, 2->1, 3->1, 4->2)

			#calculate the amount of edges fully visible in animation
			#(note that 2 edges get drawn at the same time so only half the steps are needed)
			n: int = int((len(algo_infos.solution.animation_path)+1)/2*animation_percent) #+1 => if even amount of points floor((n+1)/2) steps are needed

			#display of the first n edges going out from the middle:
			for x in range(1, n+1):
				old_left_point, new_left_point = algo_infos.solution.animation_path[mid-x+1], algo_infos.solution.animation_path[mid-x]
				pg.draw.line(main_screen, "green", old_left_point, new_left_point)
				#if even amount of points the last step only contains one edge
				if mid+x < len(algo_infos.solution.animation_path):
					old_right_point, new_right_point = algo_infos.solution.animation_path[mid+x-1], algo_infos.solution.animation_path[mid+x]
					pg.draw.line(main_screen, "green", old_right_point, new_right_point)
				
			#calculate the duration per edge in the animation
			duration_per_edge: int = int(visual_infos.animation_speed/((len(algo_infos.solution.animation_path)+1)/2))

			#draw the next edge(s) in the solution partially based on the animation_status
			if mid-n-1 >= 0:
				old_left_point, new_left_point = algo_infos.solution.animation_path[mid-n], algo_infos.solution.animation_path[mid-n-1]
				#calculate the displayed percent of the next edge
				line_percent: float = (visual_infos.animation_status % duration_per_edge)/duration_per_edge
				#interpolate the end point of the displayed edge between the actual start and end points of the next edge based on the line_percent
				np2: tuple[int, int] = sf.interpolate_on_line(old_left_point, new_left_point, line_percent)
				pg.draw.line(main_screen, "green", old_left_point, np2)
				if mid+n+1 < len(algo_infos.solution.animation_path):
					old_right_point, new_right_point = algo_infos.solution.animation_path[mid+n], algo_infos.solution.animation_path[mid+n+1]
					#interpolate the end point of the displayed edge between the actual start and end points of the next edge based on the line_percent
					np2: tuple[int, int] = sf.interpolate_on_line(old_right_point, new_right_point, line_percent)
					pg.draw.line(main_screen, "green", old_right_point, np2)
		elif (meta_infos.active_mode == 0 and algo_infos.solving_type == 0) or (meta_infos.active_mode == 1 and algo_infos.solving_type == 3):
			"""
			addbuild solving algorithm
			animation works like the 'default algorithm' but using the ordered edges provided by the algorithm
			"""
			animation_percent: float = visual_infos.animation_status/visual_infos.animation_speed
			#calculate the amount of edges fully visible in animation
			n: int = int((len(algo_infos.solution.animation_path))*animation_percent)

			#display of the first n edges:
			for x in range(n):
				p1, p2 = algo_infos.solution.animation_path[x]
				pg.draw.line(main_screen, "green", p1, p2)

			#calculate the duration per edge in the animation
			duration_per_edge: int = int(visual_infos.animation_speed/(len(algo_infos.solution.animation_path)))

			#draw the next edge in the solution partially based on the animation_status
			if len(algo_infos.solution.animation_path) > n:
				pn1, pn2 = algo_infos.solution.animation_path[n]
				#calculate the displayed percent of the next edge
				line_percent: float = (visual_infos.animation_status % duration_per_edge)/duration_per_edge
				#interpolate the end point of the displayed edge between the actual start and end points of the next edge based on the line_percent
				np2: tuple[int, int] = sf.interpolate_on_line(pn1, pn2, line_percent)
				pg.draw.line(main_screen, "green", pn1, np2)
		elif algo_infos.solving_type == 4:
			"""
			aco... work in progress
			"""
			animation_percent = visual_infos.animation_status/visual_infos.animation_speed
			#calculate the best path visible
			n = int((len(algo_infos.solution.animation_path))*animation_percent)
			visible_path = algo_infos.solution.animation_path[n]

			for x in range(len(visible_path)-1):
				p1, p2 = visible_path[x], visible_path[x+1]
				pg.draw.line(main_screen, "green", p1, p2)
	elif visual_infos.c_animation_phase == 1:
		"""
		adapts the direct solution by the instructions in adaptated_animation:
		adaptated_animation: [((start, end), before, after),...] (in solution.extra_animation_path at idx 0)
		"""
		adaptated_animation = algo_infos.solution.extra_animation_path[0]
		if len(adaptated_animation) == 0:
			#skips this animation phase
			return 1

		animation_percent = visual_infos.animation_status/visual_infos.animation_speed
		#calculate the amount of adaptations fully visible in animation
		n = int((len(adaptated_animation)+1)*animation_percent)

		#get the most recent adaptation
		if n < len(adaptated_animation):
			(start_change, end_change), last_path, _ = adaptated_animation[n]
		else:
			#last adaptation
			(start_change, end_change), last_path = (math.inf, 0), adaptated_animation[-1][2]

		#calculate the duration per adaptation in the animation
		duration_per_adaptation = int(visual_infos.animation_speed/(len(adaptated_animation)+1))

		#calculate the displayed percent of the next adaptation
		adaptation_percent = (visual_infos.animation_status % duration_per_adaptation)/duration_per_adaptation

		#draw all edges
		for idx in range(len(last_path)-1):
			p1, p2 = last_path[idx], last_path[idx+1]
			if idx >= start_change - 1 and idx <= end_change - 1:
				if idx == start_change - 1 or idx == end_change - 1:
					r, g, b = 255, 255, 0
				else:
					#interpolate the edge color of the adapted edge between green and red based on the adaptation_percent
					color1, color2 = [0,255,0], [255,0,0]
					r, g, b = sf.interpolate_list(color1, color2, adaptation_percent)
				pg.draw.line(main_screen, pg.Color(int(r),int(g),int(b)), p1, p2)
			else:
				pg.draw.line(main_screen, "green", p1, p2)
	return 0