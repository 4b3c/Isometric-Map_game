import pygame, random, math
from calculations import calculations

w_width = 1600
w_height = 900
mid_x = w_width / 2
mid_y = w_height / 2

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 50, 50)

tile_size = 40
half_tile = tile_size / 2
tile_hyp = math.sqrt((tile_size**2) + (half_tile)**2)

class tile:
	def __init__(self, coordinates, biome):
		self.coordinates = coordinates
		self.biome = biome
		self.road = False
		self.improvement = 0
		self.tile_size = 40

	def draw_tile(self, window):	
		t_x, t_y = calculations.get_window_coords(self.coordinates)
		b_y = t_y + tile_size
		l_x = t_x - tile_size
		l_y = t_y + half_tile
		r_x = t_x + tile_size
		pygame.draw.polygon(window, white, ((t_x, t_y), (l_x, l_y), (t_x, b_y), (r_x, l_y)), 2)

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
			biome = random.choice(["m", "p", "f"])
			tile_list.append(tile(coords, biome))

		return tile_list

	def draw_map(self, window):
		for tile in self.map:
			tile.draw_tile(window)