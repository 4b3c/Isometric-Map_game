import pygame, random, time, math

pygame.init()
w_width = 1100
w_height = 700
mid_x = w_width / 2
mid_y = w_height / 2
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 50, 50)
player_clicked = False
tile_size = 40
half_tile = tile_size / 2
tile_hyp = math.sqrt((tile_size**2) + (half_tile)**2)
map_size = 5
vil_coords = (0, 0)

window = pygame.display.set_mode((w_width, w_height))

#Takes an x and y on the cartesian plane and returns the intersection between
# the line which the point creates and the line which passes through the origin
def intersection(x, y, neg_coefficient):
	a1 = -0.5 * neg_coefficient
	b1 = -1
	c1 = (y + ((0.5 * x) * neg_coefficient))

	a2 = 0.5 * neg_coefficient
	b2 = -1
	c2 = 0

	x = ((b1 * c2) - (b2 * c1)) / ((a1 * b2) - (a2 * b1))
	y = ((c1 * a2) - (c2 * a1)) / ((a1 * b2) - (a2 * b1))

	return (x, y)

#Takes grid coords and spits out window coords
def grid_coords(x, y):
	t_x = (mid_x) + (x * tile_size) - (y * tile_size)
	t_y = ((mid_y) - (y * half_tile) - (x * tile_size) / 2) + half_tile

	return (t_x, t_y)

#Takes wwindow coords and is supposed to spit out grid coords
def window_coords(x, y):
	real_x = x - mid_x
	real_y = mid_y - y
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

	return (g_x, g_y)

#Takes coordinates for the isometric plane and draws them on the cartesian plane
def draw_tile(x, y):	
	t_x, t_y = grid_coords(x, y)
	b_y = t_y + tile_size
	l_x = t_x - tile_size
	l_y = t_y + half_tile
	r_x = t_x + tile_size
	pygame.draw.polygon(window, white, ((t_x, t_y), (l_x, l_y), (t_x, b_y), (r_x, l_y)), 2)

#Randomly generates a map
def generate_map():
	coord_list = [[0, 0]]
	action_list = [[1, 1], [-1, 1], [1, -1], [-1, -1]]

	for i in range(5):
		for action in action_list:
			y = 0
			while random.randint(0, abs(y * 3)) < map_size:
				x = 0
				while random.randint(0, abs(x * 3)) < map_size:
					if [x, y] not in coord_list:
						coord_list.append([x, y])
					x = x + action[0]
				y = y + action[1]

	return coord_list

class villager:

	def draw_cart_villager(self, x, y):
		x = mid_x - x
		y = mid_y - y
		self.size = [half_tile / 10, half_tile / 6]
		length, height = self.size[0], self.size[1]
		pygame.draw.rect(window, (red), (x - (length / 2), y - (height * 2.4), length, height))


	def draw_villager(self, x, y):
		x, y = grid_coords(x, y)
		self.size = [half_tile / 10, half_tile / 6]
		length, height = self.size[0], self.size[1]
		pygame.draw.rect(window, (red), (x - (length / 2), y - (height * 2.4), length, height))

	# def move_villager(start_coords, end_coords):
	# 	pass


villager1 = villager()

map = generate_map()

while True:
	window.fill(black)
	mouse_pos = pygame.mouse.get_pos()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
		elif event.type == pygame.MOUSEWHEEL:
			if event.y == 1 and 250 > tile_size:
				tile_size += tile_size / 5
				half_tile = tile_size / 2
				tile_hyp = math.sqrt((tile_size**2) + (half_tile)**2)
				mid_x = mid_x + (mid_x - mouse_pos[0]) / 5
				mid_y = mid_y + (mid_y - mouse_pos[1]) / 5
			elif event.y == -1 and 15 < tile_size:
				tile_size -= tile_size / 5
				half_tile = tile_size / 2
				tile_hyp = math.sqrt((tile_size**2) + (half_tile)**2)
				mid_x = mid_x - (mid_x - mouse_pos[0]) / 5
				mid_y = mid_y - (mid_y - mouse_pos[1]) / 5

	if pygame.mouse.get_pressed()[0]:
		mid_x = mid_x - (mouse_pos[0] - pygame.mouse.get_pos()[0])
		mid_y = mid_y - (mouse_pos[1] - pygame.mouse.get_pos()[1])
	elif pygame.mouse.get_pressed()[2]:
		vil_coords = window_coords(mouse_pos[0], mouse_pos[1])		
		
	villager1.draw_villager(vil_coords[0], vil_coords[1])
	# print(window_coords(mouse_pos[0], mouse_pos[1]))
	# villager1.draw_cart_villager(0, 0)

	for tile in map:
		draw_tile(tile[0], tile[1])

	pygame.display.flip()
	time.sleep(0.003)