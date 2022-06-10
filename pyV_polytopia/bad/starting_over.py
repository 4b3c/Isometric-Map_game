import pygame, random, math

pygame.init()
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

window = pygame.display.set_mode((w_width, w_height))



class calculations:
	def intersection(x, y, neg_coefficient):
		a1 = -0.5 * neg_coefficient
		b1 = -1
		c1 = (y + ((0.5 * x) * neg_coefficient))

		a2 = 0.5 * neg_coefficient
		b2 = -1
		c2 = 0

		x = ((b1 * c2) - (b2 * c1)) / ((a1 * b2) - (a2 * b1))
		y = ((c1 * a2) - (c2 * a1)) / ((a1 * b2) - (a2 * b1))

		return [x, y]

	def get_window_coords(coords):
		x = coords[0]
		y = coords[1]
		t_x = (mid_x) + (x * tile_size) - (y * tile_size)
		t_y = ((mid_y) - (y * half_tile) - (x * tile_size) / 2) + half_tile

		return [t_x, t_y]

	def get_grid_coords(coords):
		x = coords[0]
		y = coords[1]
		real_x = x - mid_x
		real_y = mid_y - y + 3
		negCx = 1
		negCy = 1

		if real_y < real_x / 2:
			negCy = -1
		if real_y < -real_x / 2:
			negCx = -1

		inter_x = intersection(real_x, real_y, 1)
		g_x = round(math.sqrt(((inter_x[0] - 0)**2) + ((inter_x[1] - 0)**2)) / tile_hyp) * negCx
		inter_y = intersection(real_x, real_y, -1)
		g_y = round(math.sqrt(((inter_y[0] - 0)**2) + ((inter_y[1] - 0)**2)) / tile_hyp) * negCy

		return [g_x, g_y]

class tile:
	def __init__(self, coordinates, biome):
		self.coordinates = coordinates
		self.biome = biome
		self.road = False
		self.improvement = 0

	def draw_tile(self):	
		t_x, t_y = calculations.get_window_coords(self.coordinates)
		b_y = t_y + tile_size
		l_x = t_x - tile_size
		l_y = t_y + half_tile
		r_x = t_x + tile_size
		pygame.draw.polygon(window, white, ((t_x, t_y), (l_x, l_y), (t_x, b_y), (r_x, l_y)), 2)

class map:
	def __init__(self, size):
		self.size = size
		self.plot = map.plot_map(self)
		self.map = map.generate_map(self, self.plot)

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

	def draw_map(self):
		for tile in self.map:
			tile.draw_tile()


new_map = map(8)

new_map.draw_map()

pygame.display.flip()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()