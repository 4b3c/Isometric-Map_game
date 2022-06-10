import pygame, var

pygame.font.init()

class button():
	def __init__(self, coords, text):
		self.text = text
		self.font_size = 25
		self.font = pygame.font.SysFont('Corbel', self.font_size, bold = True)
		self.pos = [coords[0], var.w_height - coords[1] - self.font_size]
		self.highlighted = False

	def draw(self, window):
		sz_x, sz_y = self.font.size(self.text)
		if self.highlighted == False:
			color = var.text_regular_color
		else:
			color = var.text_highlighted_color

		text_surface = self.font.render(self.text, False, color)
		window.blit(text_surface, self.pos)
		pygame.draw.rect(window, (color), (self.pos[0] - 3, self.pos[1] - 3, sz_x + 6, sz_y + 2), 2)

	def hovering(self, window_coords):
		x, y = window_coords
		sz_x, sz_y = self.font.size(self.text)
		if x > self.pos[0] and x < self.pos[0] + sz_x and y > self.pos[1] and y < self.pos[1] + sz_y:
			self.highlighted = True
		else:
			self.highlighted = False