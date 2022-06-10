import math, random

class check_tile():
	def __init__(self, parent, coords, end):
		self.parent = parent
		self.coords = coords
		x_dist = coords[0] - end[0]
		y_dist = coords[1] - end[1]
		self.dist = round(math.sqrt((x_dist**2) + (y_dist**2)), 1)

def return_neighbors(coords):
	action_list = [[0, 1], [0, -1], [1, 0], [-1, 0]]
	neighbors = []

	for action in action_list:
		neighbors.append([action[0] + coords[0], action[1] + coords[1]])

	return neighbors
			

def pathfind(start, end, imap):
	checking = []
	checked = []
	parents = []
	best_move = check_tile(start, start, end)
	checked.append(best_move)

	while True:
		neighbors = return_neighbors(best_move.coords)

		checked_coords = []
		for item in checked:
			checked_coords.append(item.coords)

		checking_coords = []
		for item in checking:
			checking_coords.append(item.coords)

		for neighbor in neighbors:
			if neighbor in imap.plot:
				if neighbor not in checked_coords:
					if neighbor not in checking_coords:
						checking.append(check_tile(best_move, neighbor, end))

		lowest = 1000
		for tile in checking:
			if tile not in checked:
				road_speed = imap.map[imap.plot.index(tile.coords)].road_level * 3
				if tile.dist - road_speed < lowest:
					lowest = tile.dist
					best_move = tile
					
		if best_move.coords not in checked_coords:
			checked.append(checking.pop(checking.index(best_move)))

		if best_move.coords == end:
			try:
				while True:
					parents.append(best_move.coords)
					best_move = best_move.parent
			except:
				return parents
