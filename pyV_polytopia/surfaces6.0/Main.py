import pygame, random, math, var, roads, buttons, pickle, os
from map import tile, imap
from villager import villager
from calculations import calculations

pygame.init()
window = pygame.display.set_mode((var.w_width, var.w_height))
world_file = ""
selecting_world = True
surf_pos = [0, 0]
surf_size = 1

class game:
	def __init__(self, imap, villager):
		self.map = imap
		self.villager = villager

pygame.init()
window = pygame.display.set_mode((var.w_width, var.w_height))

def select_world(window):
	worlds = os.listdir("worlds")
	world_buttons = []
	for world in worlds:
		world_buttons.append(buttons.button(30, [800, 300 - (50 * worlds.index(world))], world.replace(".pickle", ""), False))

	world_buttons.append(buttons.button(30, [800, 600], "New World", True))
	
	return world_buttons

while selecting_world:
	window.fill(var.bg)
	mouse_pos = pygame.mouse.get_pos()
	mouse_clicked = pygame.mouse.get_pressed()[0]

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()

	for button in select_world(window):
		if ".jpeg" not in button.text:
			button.run_button(mouse_pos, mouse_clicked, window)
			if button.toggle:
				if button.text == "New World":
					new_map = imap(8)
					new_villager = villager()
					selecting_world = False
					last_file = 0
					for file in os.listdir("worlds"):
						if ".jpeg" not in file:
							file = file.replace(".pickle", "")
							if int(file[-1]) > 0:
								last_file = int(file[-1])
					world_file = open("worlds\world" + str(last_file + 1) + ".pickle", "w")
					world_file.close()
					world_file = "world" + str(last_file + 1)
				else:
					world_file = button.text
					file = open("worlds\{}.pickle".format(button.text), "rb")
					pulled_data = pickle.load(file)
					file.close()
					new_map = pulled_data.map
					new_villager = pulled_data.villager
					selecting_world = False

	pygame.display.flip()

road_button = roads.roads()
path_end = [0, 0]

while True:
	window.fill(var.bg)
	mouse_pos = pygame.mouse.get_pos()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			file = open("worlds\{}.pickle".format(world_file), "wb")
			new_map.image = None
			game_obj = game(new_map, new_villager)
			pickle.dump(game_obj, file)
			file.close()
			pygame.quit()
			quit()
		elif event.type == pygame.MOUSEWHEEL:
			if event.y == 1 and 260 > var.tile_size:
				var.tile_size += var.tile_size / 5
				var.half_tile = var.tile_size / 2
				var.tile_hyp = math.sqrt((var.tile_size**2) + (var.half_tile)**2)
				var.mid_x = var.mid_x + (var.mid_x - mouse_pos[0]) / 5
				var.mid_y = var.mid_y + (var.mid_y - mouse_pos[1]) / 5
				# surf_size += surf_size / 5
				# surf_pos = [var.mid_x - (var.w_width / 2), var.mid_y - (var.w_height / 2)]
				# new_map.scale_change = True
				new_map.surface_path = "none"
			elif event.y == -1 and 40 < var.tile_size:
				var.tile_size -= var.tile_size / 5
				var.half_tile = var.tile_size / 2
				var.tile_hyp = math.sqrt((var.tile_size**2) + (var.half_tile)**2)
				var.mid_x = var.mid_x - (var.mid_x - mouse_pos[0]) / 5
				var.mid_y = var.mid_y - (var.mid_y - mouse_pos[1]) / 5
				# surf_size -= surf_size / 5
				# surf_pos = [var.mid_x - (var.w_width / 2), var.mid_y - (var.w_height / 2)]
				# new_map.scale_change = True
				new_map.surface_path = "none"

	if pygame.mouse.get_pressed()[0]:
		var.mid_x = var.mid_x - (mouse_pos[0] - pygame.mouse.get_pos()[0])
		var.mid_y = var.mid_y - (mouse_pos[1] - pygame.mouse.get_pos()[1])
		path_end = calculations.get_grid_coords(mouse_pos)
		surf_pos = [var.mid_x - (var.w_width / 2), var.mid_y - (var.w_height / 2)]
	if pygame.mouse.get_pressed()[2]:
		new_map.get_tile(mouse_pos, window)

	new_map.draw_map(window, world_file, surf_size, surf_pos)

	new_villager.move_villager(path_end, new_map)
	new_villager.draw_villager(window)
	road_button.build_roads(window, pygame.mouse.get_pressed()[0], mouse_pos, new_map)

	pygame.display.flip()
