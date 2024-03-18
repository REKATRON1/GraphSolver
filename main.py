import pygame as pg
import numpy as np

from update import update

def main() -> None:
	"""
	initialize pygame
	"""
	pg.init()
	pg.font.init()

	"""
	main program
	"""
	from update import update_info
	while update_info.running:
		update()
		pg.display.flip()

#start programm
if __name__ == '__main__':
	main()