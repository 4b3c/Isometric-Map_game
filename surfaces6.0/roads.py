import pygame, buttons, var
from calculations import calculations

class roads:
	def __init__(self):
		self.button = buttons.button(30, [100, 25], "Roads", True)

	def build_roads(self, window, mouse_clicked, mouse_pos, imap):
		if self.button.run_button(mouse_pos, mouse_clicked, window):
			g_coords = calculations.get_grid_coords(mouse_pos)
			c_coords = calculations.get_window_coords(g_coords)
			c_coords[1] = c_coords[1] - var.half_tile
			if g_coords in imap.plot:
				# pygame.draw.circle(window, var.road1, c_coords, 5)
				if mouse_clicked:
					address = imap.plot.index(g_coords)
					imap.map[address].road_level = 1




