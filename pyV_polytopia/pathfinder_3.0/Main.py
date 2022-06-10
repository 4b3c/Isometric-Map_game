import pygame, random, math, var
from map import tile, imap
from villager import villager
from calculations import calculations

pygame.init()
window = pygame.display.set_mode((var.w_width, var.w_height))

new_map = imap(8)
new_villager = villager()

path_end = [3, 4]

while True:
	window.fill(var.bg)
	mouse_pos = pygame.mouse.get_pos()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
		elif event.type == pygame.MOUSEWHEEL:
			if event.y == 1 and 600 > var.tile_size:
				var.tile_size += var.tile_size / 5
				var.half_tile = var.tile_size / 2
				var.tile_hyp = math.sqrt((var.tile_size**2) + (var.half_tile)**2)
				var.mid_x = var.mid_x + (var.mid_x - mouse_pos[0]) / 5
				var.mid_y = var.mid_y + (var.mid_y - mouse_pos[1]) / 5
			elif event.y == -1 and 5 < var.tile_size:
				var.tile_size -= var.tile_size / 5
				var.half_tile = var.tile_size / 2
				var.tile_hyp = math.sqrt((var.tile_size**2) + (var.half_tile)**2)
				var.mid_x = var.mid_x - (var.mid_x - mouse_pos[0]) / 5
				var.mid_y = var.mid_y - (var.mid_y - mouse_pos[1]) / 5

	if pygame.mouse.get_pressed()[0]:
		var.mid_x = var.mid_x - (mouse_pos[0] - pygame.mouse.get_pos()[0])
		var.mid_y = var.mid_y - (mouse_pos[1] - pygame.mouse.get_pos()[1])
		path_end = calculations.get_grid_coords(mouse_pos)

	new_villager.move_villager(path_end, new_map)

	new_map.draw_map(window)
	new_villager.draw_villager(window)

	pygame.draw.circle(window, var.red, (var.mid_x, var.mid_y), 5)

	pygame.display.flip()
