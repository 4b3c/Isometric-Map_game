import pygame, var, pathfind
from calculations import calculations

class villager:
	def __init__(self):
		self.coords_g = [0, 0]
		self.offset = [0, 0]
		self.speed = 0.25
		self.speed = [self.speed * 2, self.speed]
		self.move_count = 0
		self.path_found = False
		self.path = []

	def get_exact_coords(self):
		scale = var.half_tile / 20
		c_coords = calculations.get_window_coords(self.coords_g)
		offset = [0, 0]
		offset[0] = self.offset[0] * scale
		offset[1] = self.offset[1] * scale
		self.offset[0] = offset[0] / scale
		self.offset[1] = offset[1] / scale
		c_coords = [c_coords[0] + offset[0], c_coords[1] + offset[1] - var.half_tile]
		return c_coords

	def draw_villager(self, window):
		coords = villager.get_exact_coords(self)
		x = coords[0]
		y = coords[1]
		self.size = [var.half_tile / 4, var.half_tile / 2.5]
		length = self.size[0]
		height = self.size[1]
		pygame.draw.rect(window, var.red, (x - (length / 2), y - (height / 2), length, height))

	def move(self, targ_coords_g, map_plot):
		targ_x = targ_coords_g[0]
		targ_y = targ_coords_g[1]
		scale = var.half_tile / 20
		speed_x = self.speed[0] * var.game_speed
		speed_y = self.speed[1] * var.game_speed

		direction_x = targ_x - self.coords_g[0]
		direction_y = targ_y - self.coords_g[1]

		self.move_count = self.move_count + 1;

		if direction_x != 0:
			direction_x = direction_x / abs(direction_x)
			if [self.coords_g[0] + direction_x, self.coords_g[1]] in map_plot:

				self.offset[0] = self.offset[0] + (speed_x * direction_x)
				self.offset[1] = self.offset[1] + (-speed_y * direction_x)

				real_pos = villager.get_exact_coords(self)[0]
				square_pos = calculations.get_window_coords((self.coords_g[0] + direction_x, self.coords_g[1]))[0]
				distance = abs(abs(real_pos) - abs(square_pos))

				if distance < speed_x * 3:
					self.coords_g[0] = calculations.get_grid_coords(villager.get_exact_coords(self))[0]
					self.offset = [0, 0]

		elif direction_y != 0:
			direction_y = direction_y / abs(direction_y)
			if [self.coords_g[0], self.coords_g[1] + direction_y] in map_plot:

				self.offset[0] = self.offset[0] + (-speed_x * direction_y)
				self.offset[1] = self.offset[1] + (-speed_y * direction_y)

				real_pos = villager.get_exact_coords(self)[1]
				square_pos = calculations.get_window_coords((self.coords_g[0], self.coords_g[1] + direction_y))[1] - var.half_tile
				distance = abs(abs(real_pos) - abs(square_pos))

				if distance < speed_y * 3:
					self.coords_g[1] = calculations.get_grid_coords(villager.get_exact_coords(self))[1]
					self.offset = [0, 0]

	def move_villager(self, target, imap):
		if self.coords_g != target:
			if self.path_found == True:
				if self.coords_g == self.path[-1]:
					self.path.remove(self.coords_g)
				if len(self.path) > 0:
					villager.move(self, self.path[-1], imap.plot)
				else:
					self.path_found = False
			else:
				if target in imap.plot:
					self.path = pathfind.pathfind(self.coords_g, target, imap)
					self.path_found = True
		else:
			pass







		# if self.coords_g != target:
		# 	if self.path_found == True:
		# 		if self.coords_g in self.path:
		# 			villager.move(self, self.path[0], imap.plot)
		# 			if self.coords_g == self.path[0]:
		# 				self.path.remove(self.coords_g)
		# 		else:
		# 			villager.move(self, self.path[0], imap.plot)
		# 	else:
		# 		self.path = pathfind.pathfind(self.coords_g, target, imap)
		# 		self.path_found = True
		# else:
		# 	self.path_found = False

		# 		