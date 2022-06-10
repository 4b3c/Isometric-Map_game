import pygame

pygame.init()

window = pygame.display.set_mode((900, 600))
white = (255, 255, 255)
size = width, height = (700, 500)
empty_surface = pygame.Surface(size)
empty_surface.fill(white)
image = pygame.image.load("wallpaper.jpg").convert()
empty_surface.blit(image, (0, 0))
window.blit(empty_surface, (20, 20))
pygame.image.save(window, "screenshot.jpeg")
real_surface = pygame.Surface((900, 600))
image = pygame.image.load("screenshot.jpeg").convert()
real_surface.blit(image, (0, 0))

size = (40, 40)
second_surface = pygame.Surface(size)
second_surface.fill(white)

direction = .1
pos = [10, 300]


while True:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()

	if pos[0] < 10:
		direction = .1
	elif pos[0] > 590:
		direction = -.1

	pos[0] = pos[0] + direction
	print(pos)

	window.blit(real_surface, (0, 0))
	window.blit(second_surface, pos)

	pygame.display.flip()
