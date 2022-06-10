import pygame, random, time, math

pygame.init()
w_width = 1600
w_height = 900
mid_x = w_width / 2
mid_y = w_height / 2
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 50, 50)
player_clicked = False
tile_size = 40
half_tile = tile_size / 2
tile_hyp = math.sqrt((tile_size**2) + (half_tile)**2)
map_size = 8
vil_coords = (0, 0)
start_coords = [0, 0]
end_coords = [0, 0]

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

	return [x, y]

#Takes grid coords and spits out window coords
def get_window_coords(coords):
	x = coords[0]
	y = coords[1]
	t_x = (mid_x) + (x * tile_size) - (y * tile_size)
	t_y = ((mid_y) - (y * half_tile) - (x * tile_size) / 2) + half_tile

	return [t_x, t_y]

#Takes window coords and is supposed to spit out grid coords
def get_grid_coords(coords):
	x = coords[0]
	y = coords[1]
	real_x = x - mid_x
	#the +3 makes everything work, don't question it, don't remove it, just let it be
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

#Takes coordinates for the isometric plane and draws them on the cartesian plane
def draw_tile(x, y):	
	t_x, t_y = get_window_coords((x, y))
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

	def __init__(self):
		self.coords_g = [0, 0]
		self.offset = [0, 0]
		self.speed = 0.2
		self.speed = [self.speed * 2, self.speed]
		self.move_count = 0
		self.last_scale = 1

	def get_exact_coords(self):
		scale = half_tile / 20
		c_coords = get_window_coords(self.coords_g)
		offset = [0, 0]
		offset[0] = self.offset[0] * scale
		offset[1] = self.offset[1] * scale
		self.offset[0] = offset[0] / scale
		self.offset[1] = offset[1] / scale
		c_coords = [c_coords[0] + offset[0], c_coords[1] + offset[1] - half_tile]
		return c_coords

	def draw_villager(self):
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
			if round(villager.get_exact_coords(self)[0]) == round(get_window_coords((self.coords_g[0] + direction_x, self.coords_g[1]))[0]):
				self.coords_g[0] = get_grid_coords(villager.get_exact_coords(self))[0]
				self.offset = [0, 0]

		# We use an elif so that it only moves in the Y direction once it's lined up on the X
		# This let's it go in straight lines to the place it wants to go
		elif direction_y != 0:
			direction_y = direction_y / abs(direction_y)

			self.offset[0] = self.offset[0] + (-speed_x * direction_y)
			self.offset[1] = self.offset[1] + (-speed_y * direction_y)

			if round(villager.get_exact_coords(self)[1]) == round(get_window_coords((self.coords_g[0], self.coords_g[1] + direction_y))[1] - half_tile):
				self.coords_g[1] = get_grid_coords(villager.get_exact_coords(self))[1]
				self.offset = [0, 0]

villager1 = villager()
villager1.coords_g = [0, 0]
map = generate_map()

while True:
	window.fill(black)
	mouse_pos = pygame.mouse.get_pos()
	mouse_tile_pos = get_grid_coords(mouse_pos)

	villager1.draw_villager()
	for tile in map:
		draw_tile(tile[0], tile[1])

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
		elif event.type == pygame.MOUSEWHEEL:
			if event.y == 1 and 700 > tile_size:
				tile_size += tile_size / 5
				half_tile = tile_size / 2
				tile_hyp = math.sqrt((tile_size**2) + (half_tile)**2)
				mid_x = mid_x + (mid_x - mouse_pos[0]) / 5
				mid_y = mid_y + (mid_y - mouse_pos[1]) / 5
			elif event.y == -1 and 5 < tile_size:
				tile_size -= tile_size / 5
				half_tile = tile_size / 2
				tile_hyp = math.sqrt((tile_size**2) + (half_tile)**2)
				mid_x = mid_x - (mid_x - mouse_pos[0]) / 5
				mid_y = mid_y - (mid_y - mouse_pos[1]) / 5

	if pygame.mouse.get_pressed()[0]:
		mid_x = mid_x - (mouse_pos[0] - pygame.mouse.get_pos()[0])
		mid_y = mid_y - (mouse_pos[1] - pygame.mouse.get_pos()[1])
		villager1.move_villager(get_grid_coords(mouse_pos))

	pygame.display.flip()
	time.sleep(0.003)