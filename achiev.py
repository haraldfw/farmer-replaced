import util

def water_achiev():
	set_world_size(4)
	ws = get_world_size()
	startx = 0
	starty = 0
	endx = 4
	endy = 4
	for x in range(startx, endx):
		util.move_to_x(x)
		range_start = starty
		range_end = endy
		step = 1
		if (x-startx)%2 != 0:
			range_start = endy-1
			range_end = starty-1
			step = -1
		for y in range(range_start, range_end, step):
			util.move_to_y(y, ws)
			util.water_to(0.75)

if __name__ == "__main__":
	water_achiev()
	recurse()