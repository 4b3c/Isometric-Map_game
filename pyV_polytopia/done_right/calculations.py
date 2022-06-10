import math

w_width = 1600
w_height = 900
mid_x = w_width / 2
mid_y = w_height / 2

tile_size = 40
half_tile = tile_size / 2
tile_hyp = math.sqrt((tile_size**2) + (half_tile)**2)

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

		inter_x = calculations.intersection(real_x, real_y, 1)
		g_x = round(math.sqrt(((inter_x[0] - 0)**2) + ((inter_x[1] - 0)**2)) / tile_hyp) * negCx
		inter_y = calculations.intersection(real_x, real_y, -1)
		g_y = round(math.sqrt(((inter_y[0] - 0)**2) + ((inter_y[1] - 0)**2)) / tile_hyp) * negCy

		return [g_x, g_y]