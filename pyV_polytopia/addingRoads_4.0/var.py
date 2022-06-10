import math

tile_size = 40
half_tile = tile_size / 2
tile_hyp = math.sqrt((tile_size**2) + (half_tile)**2)

w_width = 1600
w_height = 900
mid_x = w_width / 2
mid_y = w_height / 2

game_speed = 1

bg = (20, 20, 20)
white = (255, 255, 255)
red = (255, 50, 50)
dark_green = (5, 110, 20)
light_green = (100, 175, 40)
tan = (165, 150, 140)
gray = (125, 125, 140)
text_regular_color = (170, 170, 170)
text_highlighted_color = (250, 250, 250)
road1 = (170, 200, 225)

biomes = {
	"m": gray,
	"p": light_green,
	"f": dark_green,
	"d": tan
}