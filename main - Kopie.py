import pygame as pg
import numpy as np

from extra import datacompression
from ui import visualaddons
from ui import screenmanager
from ui import inputmanager

def __main__():
	"""
	initialize pygame + used fonts
	"""
	pg.init()
	pg.font.init()
	fps_clock = pg.time.Clock()

	meta_infos = datacompression.MetaInfos()
	meta_infos.main_font = pg.font.SysFont('Comic Sans MS', 20)

	algo_infos = datacompression.AlgoInfos()
	visual_infos = datacompression.VisualInfos(meta_infos)
	main_screen = pg.display.set_mode(meta_infos.screen_size, pg.RESIZABLE)

	"""
	main program
	"""
	while meta_infos.running:
		"""
		test for window resizing
		"""
		visual_infos.update_window_sizes(main_screen, meta_infos)
		"""
		key-input handling
		"""
		for event in pg.event.get():
			if event.type == pg.QUIT:
				meta_infos.running = False
			if event.type == pg.KEYDOWN:
				inputmanager.get_key_inputs(pg.key.get_pressed(), meta_infos, algo_infos, visual_infos)
		"""
		initialize screen
		"""
		#fill background
		main_screen.fill("black")

		"""
		mouse handling
		"""
		inputmanager.get_mouse_inputs(meta_infos, algo_infos, visual_infos)
		
		"""
		draw points
		"""
		for point in algo_infos.points:
			pg.draw.circle(main_screen, "red", point, visual_infos.point_size)

		"""
		draw (and animate?) solved path (if one is available)
		"""
		screenmanager.draw_solution(main_screen, meta_infos, algo_infos, visual_infos)
		
		"""
		draw UI on screen
		"""
		screenmanager.draw_screen(main_screen, meta_infos, algo_infos, visual_infos)

		"""
		update pygame-display and meta-stats
		"""
		pg.display.flip()
		meta_infos.delta_time = fps_clock.tick(meta_infos.tick_rate) / 1000

__main__() #start programm