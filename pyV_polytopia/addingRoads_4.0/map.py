import pygame, random, math, var, pathfind
from calculations import calculations

class tile:
	def __init__(self, coordinates, biome):
		self.coordinates = coordinates
		self.biome = biome
		self.road_level = 0
		self.improvement = 0

	def draw_tile(self, window, tile_obj_neighbors):	
		t_x, t_y = calculations.get_window_coords((self.coordinates[0] + 1, self.coordinates[1] + 1))
		b_y = t_y + var.tile_size
		l_x = t_x - var.tile_size
		l_y = t_y + var.half_tile
		r_x = t_x + var.tile_size
		pygame.draw.polygon(window, var.biomes[self.biome], ((t_x, t_y), (l_x, l_y), (t_x, b_y), (r_x, l_y)))
		pygame.draw.polygon(window, var.white, ((t_x, t_y), (l_x, l_y), (t_x, b_y), (r_x, l_y)), 2)
		if self.road_level != 0:
			if len(tile_obj_neighbors) == 0:
				pygame.draw.circle(window, var.road1, (t_x, l_y), 4)
				
			else:
				for neighbor in tile_obj_neighbors:
					t_pos = calculations.get_window_coords(self.coordinates)
					t_pos = [t_pos[0], t_pos[1] - 2 - var.half_tile]
					t_pos2 = [t_pos[0], t_pos[1] + 4]
					n_pos = calculations.get_window_coords(neighbor.coordinates)
					n_pos = [n_pos[0], n_pos[1] - 2 - var.half_tile]
					n_pos2 = [n_pos[0], n_pos[1] + 4]
					pygame.draw.polygon(window, var.road1, (t_pos, t_pos2, n_pos2, n_pos))

class imap:
	def __init__(self, size):
		self.size = size
		self.plot = imap.plot_map(self)
		self.map = imap.generate_map(self, self.plot)

	def plot_map(self):
		coord_list =  [[0, 0]]
		action_list = [[1, 1], [-1, 1], [1, -1], [-1, -1]]

		for i in range(6):
			for action in action_list:
				y = 0
				while random.randint(0, abs(y * 3)) < self.size:
					x = 0
					while random.randint(0, abs(x * 3)) < self.size:
						if [x, y] not in coord_list:
							coord_list.append([x, y])
						x = x + action[0]
					y = y + action[1]

		return coord_list

	def generate_map(self, plot):
		tile_list = []
		for coords in plot:
			biome = random.choice(["m", "p", "f", "d"])
			tile_list.append(tile(coords, biome))

		return tile_list

	def draw_map(self, window):
		for tile in self.map:
			tile_obj_neighbors = []
			neighbors = pathfind.return_neighbors(tile.coordinates)
			for neighbor in neighbors:
				if neighbor in self.plot:
					address = self.plot.index(neighbor)
					if self.map[address].road_level != 0:
						tile_obj_neighbors.append(self.map[address])

				tile.draw_tile(window, tile_obj_neighbors)