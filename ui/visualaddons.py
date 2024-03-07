import pygame as pg
import math

class Sidebar():
	def __init__(self, left_edge_x: int, right_edge_x: int, top_texts: list[str], fixed_bottom_texts: list[str], size: int=40):
		self.left_edge_x: int = left_edge_x
		self.right_edge_x: int = right_edge_x
		self.top_texts: list[str] = top_texts
		self.not_visible_txt_idx: int = math.inf
		self.fixed_bottom_texts: list[str] = fixed_bottom_texts
		self.size: int = size

	def draw(self, main_screen, meta_infos) -> None:
		if self.left_edge_x > 0:
			pg.draw.line(main_screen, "white", (self.left_edge_x, 0), (self.left_edge_x, meta_infos.screen_size[1]))
		if self.right_edge_x < main_screen.get_width()-1:
			pg.draw.line(main_screen, "white", (self.right_edge_x, 0), (self.right_edge_x, meta_infos.screen_size[1]))

		min_y: float = math.inf
		for dy, txt in enumerate(self.fixed_bottom_texts):
			y: float = -(.5 + dy)*self.size + main_screen.get_height()
			if y < 0:
				min_y = 0
				break
			min_y = y - self.size//2
			x: float = self.left_edge_x + 0.5*(self.right_edge_x - self.left_edge_x)
			color: str = "white"
			if txt == 'Solve':
				color = "black"
			elif meta_infos.get_button_activity(txt):
				color = "green"
			text_surface = meta_infos.main_font.render(txt, False, color)
			text_rect = text_surface.get_rect(center=(x, y))
			main_screen.blit(text_surface, text_rect)

		for dy, txt in enumerate(self.top_texts):
			y: float = (.5 + dy)*self.size
			if y >= min_y:
				self.not_visible_txt_idx = dy
				break
			else:
				self.not_visible_txt_idx = dy + 1
			x: float = self.left_edge_x + 0.5*(self.right_edge_x - self.left_edge_x)
			color: str = "white"
			if meta_infos.get_button_activity(txt):
				color = "green"
			text_surface = meta_infos.main_font.render(txt, False, color)
			text_rect = text_surface.get_rect(center=(x, y))
			main_screen.blit(text_surface, text_rect)

	def get_buttons(self, meta_infos, algo_infos) -> list[tuple[str, pg.Rect]]:
		buttons: list[tuple[str, pg.Rect]] = []
		left_x: float = self.left_edge_x + .05*(self.right_edge_x - self.left_edge_x)
		buttons_width: float = .9*(self.right_edge_x - self.left_edge_x)
		for dy, txt in enumerate(self.top_texts):
			if dy < self.not_visible_txt_idx:
				y = dy*self.size
				top_left = (left_x, y)
				buttons.append((txt, pg.Rect(top_left, (buttons_width, self.size))))
		bottom_buttons: list[tuple[str, pg.Rect]] = []
		for dy, txt in enumerate(self.fixed_bottom_texts):
			y = -(1 + dy)*self.size + meta_infos.screen_size[1]
			if y < 0:
				break
			top_left = (left_x, y)
			bottom_buttons.append((txt, pg.Rect(top_left, (buttons_width, self.size))))
		buttons.extend(bottom_buttons[::-1])
		return buttons

class Bar():
	def __init__(self, texts: list[str], top_left_corner: tuple[int, int], max_bottom_right_corner: tuple[int, int], size: int=40,
					alignment_mode: int=0, centralized: tuple[bool, bool]=(False, False), row_aligned: bool=True, draw_separation: bool=False):
		self.top_left_corner: tuple[int, int] = top_left_corner
		self.max_bottom_right_corner: tuple[int, int] = max_bottom_right_corner
		self.texts: list[str] = texts
		self.size: int = size
		self.alignment_mode: int = alignment_mode
		match alignment_mode:
			case 0 | 2:
				self.row_aligned: bool = True
				self.centralized: tuple[bool, bool] = (True, False)
			case 1 | 3:
				self.row_aligned: bool = False
				self.centralized: tuple[bool, bool] = (False, True)
			case _:
				self.row_aligned: bool = row_aligned
				self.centralized: tuple[bool, bool] = centralized
		self.draw_separation: bool = draw_separation

		self.buttons: list[tuple[str, pg.Rect]] = []

	def draw(self, main_screen, meta_infos) -> None:
		self.buttons = []
		width_buffer: float = 5.0
		height_buffer: float = 5.0

		match self.alignment_mode:
			case 0:
				#top
				top_left_corner: tuple[int, int] = (0,0)
				max_bottom_right_corner: tuple[int, int] = meta_infos.screen_size
			case 1:
				#left
				top_left_corner: tuple[int, int] = (0,0)
				max_bottom_right_corner: tuple[int, int] = meta_infos.screen_size
			case 2:
				#bottom
				top_left_corner: tuple[int, int] = (0, meta_infos.screen_size[1]-2*self.size/height_buffer-meta_infos.main_font.render('Test', False, "white").get_rect().height)
				max_bottom_right_corner: tuple[int, int] = meta_infos.screen_size
			case 3:
				#right
				top_left_corner: tuple[int, int] = (meta_infos.screen_size[0]-max([meta_infos.main_font.render(x, False, "white").get_rect().width+self.size/width_buffer*2 for x in self.texts]), 0)
				max_bottom_right_corner: tuple[int, int] = meta_infos.screen_size
			case _:
				#fixed
				top_left_corner: tuple[int, int] = self.top_left_corner
				max_bottom_right_corner: tuple[int, int] = self.max_bottom_right_corner		

		if self.row_aligned:
			width: float = min(max_bottom_right_corner[0]-top_left_corner[0],
						sum([meta_infos.main_font.render(x, False, "white").get_rect().width+self.size/width_buffer*self.draw_separation for x in self.texts])+self.size/width_buffer*(4-self.draw_separation))
			height: float = min(max_bottom_right_corner[1]-top_left_corner[1],
						max([meta_infos.main_font.render(x, False, "white").get_rect().height+self.size/height_buffer*2 for x in self.texts]))
		else:
			width: float = min(max_bottom_right_corner[0]-top_left_corner[0],
						max([meta_infos.main_font.render(x, False, "white").get_rect().width+self.size/width_buffer*2 for x in self.texts]))
			height: float = min(max_bottom_right_corner[1]-top_left_corner[1],
						sum([meta_infos.main_font.render(x, False, "white").get_rect().height+self.size/height_buffer*self.draw_separation for x in self.texts])+self.size/height_buffer*(4-self.draw_separation))
		
		if self.centralized[0] or self.centralized[1]:
			center: tuple[float, float] = (max_bottom_right_corner[0]-top_left_corner[0])/2, (max_bottom_right_corner[1]-top_left_corner[1])/2
			bar_rect: pg.Rect = pg.Rect((0,0), (width, height))
			bar_rect.center = center
			if not self.centralized[0]:
				bar_rect.left = top_left_corner[0]
			elif not self.centralized[1]:
				bar_rect.top = top_left_corner[1]
		else:
			bar_rect = pg.Rect(top_left_corner, (width, height))

		if bar_rect.left > 0:
			pg.draw.line(main_screen, "white", (bar_rect.left, bar_rect.top), (bar_rect.left, bar_rect.bottom))
		if bar_rect.right < main_screen.get_width()-1:
			pg.draw.line(main_screen, "white", (bar_rect.right, bar_rect.top), (bar_rect.right, bar_rect.bottom))
		if bar_rect.top > 0:
			pg.draw.line(main_screen, "white", (bar_rect.left, bar_rect.top), (bar_rect.right, bar_rect.top))
		if bar_rect.bottom < main_screen.get_height()-1:
			pg.draw.line(main_screen, "white", (bar_rect.left, bar_rect.bottom), (bar_rect.right, bar_rect.bottom))
		
		cX, cY = bar_rect.left+self.size/width_buffer, bar_rect.top+self.size/height_buffer
		current_text_index: int = 0
		while cX < bar_rect.right and cY < bar_rect.bottom and current_text_index < len(self.texts):
			txt: str = self.texts[current_text_index]
			text_rect = meta_infos.main_font.render(txt, False, "white").get_rect()
			text_rect.left, text_rect.top = cX, cY

			if self.row_aligned:
				if current_text_index > 0:
					if self.draw_separation:
						cX += self.size/width_buffer
						pg.draw.line(main_screen, "white", (cX, bar_rect.top), (cX, bar_rect.bottom))
					cX += self.size/width_buffer
				text_rect.left = cX
				if cX + self.size/width_buffer + text_rect.width > bar_rect.right:
					break
				cX += text_rect.width
			else:
				if current_text_index > 0:
					cY += self.size/height_buffer
					if self.draw_separation:
						pg.draw.line(main_screen, "white", (bar_rect.left, cY), (bar_rect.right, cY))
						cY += self.size/height_buffer
				text_rect.top = cY
				if cY + self.size/height_buffer + text_rect.height > bar_rect.bottom:
					break
				self.buttons.append((txt, text_rect))
				cY += text_rect.height

			if meta_infos.get_button_activity(txt):
				color: str = "green"
			else:
				color: str = "white"

			self.buttons.append((txt, text_rect))
			text_surface = meta_infos.main_font.render(txt, False, color)
			main_screen.blit(text_surface, text_rect)

			current_text_index += 1


	def get_buttons(self) -> list[tuple[str, pg.Rect]]:
		return self.buttons