import pygame
from calculations import calculations

tile_size = 40
half_tile = tile_size / 2

red = (255, 50, 50)

class villager:
	def __init__(self):
		self.coords_g = [0, 0]
		self.offset = [0, 0]
		self.speed = 0.275
		self.speed = [self.speed * 2, self.speed]
		self.move_count = 0
		self.last_scale = 1

	def get_exact_coords(self):
		scale = half_tile / 20
		c_coords = calculations.get_window_coords(self.coords_g)
		offset = [0, 0]
		offset[0] = self.offset[0] * scale
		offset[1] = self.offset[1] * scale
		self.offset[0] = offset[0] / scale
		self.offset[1] = offset[1] / scale
		c_coords = [c_coords[0] + offset[0], c_coords[1] + offset[1] - half_tile]
		return c_coords

	def draw_villager(self, window):
		coords = villager.get_exact_coords(self)
		x = coords[0]
		y = coords[1]
		self.size = [half_tile / 4, half_tile / 2.5]
		length = self.size[0]
		height = self.size[1]
		pygame.draw.rect(window, (red), (x - (length / 2), y - (height / 2), length, height))

	def move_villager(self, targ_coords_g):
		# Get the target grid coordinates
		targ_x = targ_coords_g[0]
		targ_y = targ_coords_g[1]
		# Get the scale of how much we're zoomed in
		scale = half_tile / 20
		# Set the speed to be faster when we're zoomed in so the movement seems the same in comparison to size
		speed_x = self.speed[0]
		speed_y = self.speed[1]

		# The direction is dependant on which is bigger, the target coordinates or the current coordinates
		direction_x = targ_x - self.coords_g[0]
		direction_y = targ_y - self.coords_g[1]

		self.move_count = self.move_count + 1;

		# If the direction in the X is not zero, it means we have to move
		if direction_x != 0:
			# This sets the direction to either be 1 or negative 1 depending on which way we have to go
			direction_x = direction_x / abs(direction_x)

			# The offset is how far from the center of the current grid square it is in
			# [0] = X, [1] = Y We increase them both in order to move diagonaly
			self.offset[0] = self.offset[0] + (speed_x * direction_x)
			self.offset[1] = self.offset[1] + (-speed_y * direction_x)

			# If we offset the villager so much that it's in the center of the next square, change the grid coordinates to said square's coordinates
			# Once we change the grid coordinates, we also change the offset to [0, 0]
			if round(villager.get_exact_coords(self)[0]) == round(calculations.get_window_coords((self.coords_g[0] + direction_x, self.coords_g[1]))[0]):
				self.coords_g[0] = calculations.get_grid_coords(villager.get_exact_coords(self))[0]
				self.offset = [0, 0]

		# We use an elif so that it only moves in the Y direction once it's lined up on the X
		# This let's it go in straight lines to the place it wants to go
		elif direction_y != 0:
			direction_y = direction_y / abs(direction_y)

			self.offset[0] = self.offset[0] + (-speed_x * direction_y)
			self.offset[1] = self.offset[1] + (-speed_y * direction_y)

			if round(villager.get_exact_coords(self)[1]) == round(calculations.get_window_coords((self.coords_g[0], self.coords_g[1] + direction_y))[1] - half_tile):
				self.coords_g[1] = calculations.get_grid_coords(villager.get_exact_coords(self))[1]
				self.offset = [0, 0]