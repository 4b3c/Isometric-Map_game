import pygame, var

pygame.font.init()

class button():
	def __init__(self, size, coords, text, bold):
		self.text = text
		self.font_size = size
		self.font = pygame.font.SysFont('Corbel', self.font_size, bold)
		self.pos = [coords[0] - (self.font.size(text)[0] / 2), var.w_height - coords[1] - self.font_size]
		self.highlighted = False
		self.toggle = False
		self.open = False

	def draw(self, window):
		sz_x, sz_y = self.font.size(self.text)
		if self.highlighted or self.open:
			color = var.text_highlighted_color
		else:
			color = var.text_regular_color

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

	def toggler(self, mouse_clicked):
		if self.highlighted:
			if mouse_clicked == True:
				self.toggle = True
			elif self.toggle and mouse_clicked == False:
				self.toggle = False
				if self.open:
					self.open = False
				else:
					self.open = True

	def run_button(self, window_coords, mouse_clicked, window):
		button.hovering(self, window_coords)
		button.draw(self, window)
		button.toggler(self, mouse_clicked)
		return self.open

