import pygame, random, time

pygame.init()
w_width = 1100
w_height = 700
mid_x = w_width / 2
mid_y = w_height / 2
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 50, 50)
blue = (60, 80, 140)
tile_size = 80
map_size = 5

window = pygame.display.set_mode((w_width, w_height))

def draw_tile(x, y, landscape):	
	l_x = (mid_x) + (x * tile_size) - (y * tile_size) - tile_size
	t_y = (mid_y) - (y * tile_size / 2) - (x * tile_size) / 2
	if (landscape == "H"):
		hills_image = pygame.image.load(r"C:\Users\Abram P\Desktop\Python_scripts\pyV_polytopia\images\hills.png")
		hills_image = pygame.transform.scale(hills_image, (int(tile_size) * 2, int(tile_size)))
		window.blit(hills_image, (l_x, t_y))
	elif (landscape == "M"):
		mountains_image = pygame.image.load(r"C:\Users\Abram P\Desktop\Python_scripts\pyV_polytopia\images\mountain.png")
		mountains_image = pygame.transform.scale(mountains_image, (int(tile_size) * 2, int(tile_size)))
		window.blit(mountains_image, (l_x, t_y))
	elif (landscape == "G"):
		grasslands_image = pygame.image.load(r"C:\Users\Abram P\Desktop\Python_scripts\pyV_polytopia\images\grasslands.png")
		grasslands_image = pygame.transform.scale(grasslands_image, (int(tile_size) * 2, int(tile_size)))
		window.blit(grasslands_image, (l_x, t_y))

def generate_map():
	coord_list = []
	action_list = [[1, 1], [-1, 1], [1, -1], [-1, -1]]

	for i in range(5):
		for action in action_list:
			y = 0
			while random.randint(0, abs(y * 3)) < map_size:
				x = 0
				while random.randint(0, abs(x * 3)) < map_size:
					if [x, y] not in coord_list:
						coord_list.append([x, y, random.choice(["M", "H", "G"])])
					x = x + action[0]
				y = y + action[1]

	return coord_list

map = generate_map()

while True:
	window.fill(blue)
	mouse_pos = pygame.mouse.get_pos()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
		elif event.type == pygame.MOUSEWHEEL:
			if event.y == 1 and 350 > tile_size:
				tile_size += tile_size / 5
				mid_x = mid_x + (mid_x - mouse_pos[0]) / 5
				mid_y = mid_y + (mid_y - mouse_pos[1]) / 5
			elif event.y == -1 and 15 < tile_size:
				tile_size -= tile_size / 5
				mid_x = mid_x - (mid_x - mouse_pos[0]) / 5
				mid_y = mid_y - (mid_y - mouse_pos[1]) / 5

	if pygame.mouse.get_pressed()[0]:
		mid_x = mid_x - (mouse_pos[0] - pygame.mouse.get_pos()[0])
		mid_y = mid_y - (mouse_pos[1] - pygame.mouse.get_pos()[1])

	for tile in map:
		draw_tile(tile[0], tile[1], tile[2])
	
	pygame.display.flip()
	time.sleep(0.003)