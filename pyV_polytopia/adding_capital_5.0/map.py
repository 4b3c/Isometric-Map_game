import pygame, random, math, var, pathfind
from calculations import calculations

class tile:
	def __init__(self, coordinates, biome):
		self.coordinates = coordinates
		self.biome = biome
		self.road_level = 0
		self.building = 0

	def draw_tile(self, surface, tile_obj_neighbors):	
		t_x, t_y = calculations.get_window_coords((self.coordinates[0] + 1, self.coordinates[1] + 1))
		b_y = t_y + var.tile_size
		l_x = t_x - var.tile_size
		l_y = t_y + var.half_tile
		r_x = t_x + var.tile_size
		if t_x > var.tile_size * -1 and t_x < var.w_width + var.tile_size and t_y > var.tile_size * -1 and t_y < var.w_height + var.tile_size:
			pygame.draw.polygon(surface, var.biomes[self.biome], ((t_x, t_y), (l_x, l_y), (t_x, b_y), (r_x, l_y)))
			pygame.draw.polygon(surface, var.white, ((t_x, t_y), (l_x, l_y), (t_x, b_y), (r_x, l_y)), 2)
			#pygame.draw.polygon(surface, var.biomes[self.biome], ((t_x, t_y), (t_x + 20, t_y + 10), (t_x, t_y + 20), (t_x - 20, t_y + 10)))
		if self.road_level != 0:
			if len(tile_obj_neighbors) == 0:
				pygame.draw.circle(surface, var.road1, (t_x, l_y), 4)
				
			else:
				for neighbor in tile_obj_neighbors:
					t_pos = calculations.get_window_coords(self.coordinates)
					t_pos = [t_pos[0], t_pos[1] - 2 - var.half_tile]
					t_pos2 = [t_pos[0], t_pos[1] + 4]
					n_pos = calculations.get_window_coords(neighbor.coordinates)
					n_pos = [n_pos[0], n_pos[1] - 2 - var.half_tile]
					n_pos2 = [n_pos[0], n_pos[1] + 4]
					pygame.draw.polygon(surface, var.road1, (t_pos, t_pos2, n_pos2, n_pos))

class imap:
	def __init__(self, size):
		self.size = size
		self.plot = imap.plot_map(self)
		self.map = imap.generate_map(self, self.plot)
		self.surface_path = "none"
		self.image = None
		self.scale_change = False

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
			biome = random.choice(["Mountain", "Plains", "Forrest", "Desert"])
			if coords == [0, 0]:
				biome = "Capital"
			tile_list.append(tile(coords, biome))

		return tile_list

	def draw_map(self, window, world_name, surf_size, surf_pos):
		if self.surface_path == "none":
			self.image = pygame.Surface((var.w_width * 3, var.w_height * 3))
			self.image = pygame.transform.scale(self.image, (var.w_width, var.w_height))
			self.image.fill(var.bg)
			for tile in self.map:
				tile_obj_neighbors = []
				neighbors = pathfind.return_neighbors(tile.coordinates)
				for neighbor in neighbors:
					if neighbor in self.plot:
						address = self.plot.index(neighbor)
						if self.map[address].road_level != 0:
							tile_obj_neighbors.append(self.map[address])

					tile.draw_tile(self.image, tile_obj_neighbors)

			self.surface_path = "worlds\{}map_surface.jpeg".format(world_name)
			pygame.image.save(self.image, self.surface_path)
		elif self.image == None:
			self.surface_path = "worlds\{}map_surface.jpeg".format(world_name)
			self.image = pygame.image.load(self.surface_path)
		else:
			if self.scale_change == True:
				self.image = pygame.image.load(self.surface_path)
				self.image = pygame.transform.scale(self.image, (int(var.w_width * surf_size), int(var.w_height * surf_size)))
				self.scale_change = False
			window.blit(self.image, surf_pos)


	def draw_text(pos, text, window, bold):
		font_size = 25
		font = pygame.font.SysFont('Corbel', font_size, bold = bold)
		text_surface = font.render(text, False, var.white)
		window.blit(text_surface, pos)

	def get_tile(self, mouse_pos, window):
		g_coords = calculations.get_grid_coords(mouse_pos)
		if g_coords in self.plot:
			text1 = self.map[self.plot.index(g_coords)].biome + " " + str(g_coords)
			text2 = "Road - " + str(self.map[self.plot.index(g_coords)].road_level)
			text3 = "Improvements - " + str(self.map[self.plot.index(g_coords)].building)
			imap.draw_text([1400, 800], text1, window, True)
			imap.draw_text([1400, 835], text2, window, False)
			imap.draw_text([1400, 865], text3, window, False)


