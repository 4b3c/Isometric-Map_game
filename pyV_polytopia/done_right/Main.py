import pygame, random, math
from map import tile, imap
from villager import villager
from calculations import calculations

pygame.init()
w_width = 1600
w_height = 900
bg = (10, 10, 40)
window = pygame.display.set_mode((w_width, w_height))

new_map = imap(8)
new_villager = villager()

while True:
	window.fill(bg)
	mouse_pos = pygame.mouse.get_pos()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()

	if pygame.mouse.get_pressed()[0]:
		new_villager.move_villager(calculations.get_grid_coords(mouse_pos))

	new_map.draw_map(window)
	new_villager.draw_villager(window)

	pygame.display.update()