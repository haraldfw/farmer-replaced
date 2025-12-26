import util
# TODO: flip movement along Y depending on even-ness of X, so that we end our snake in the top Right

def sort_north_south(y, starty, endy):
	unsorted_found = False
	here = measure()
	north = None
	if y < endy:
		north = measure(North)

	south = None
	if y > starty:
		south = measure(South)
	
	if north != None and here > north:
		unsorted_found = True
		swap(North)
		t = north
		north = here
		here = t
	
	if south != None and here < south:
		unsorted_found = True
		swap(South)
	
	return unsorted_found

def sort_east_west(x, startx, endx):
	unsorted_found = False
	here = measure()
	east = None
	if x < endx:
		east = measure(East)

	west = None
	if x > startx:
		west = measure(West)
	
	if east != None and here > east:
		unsorted_found = True
		swap(East)
		t = east
		east = here
		here = t
	
	if west != None and here < west:
		unsorted_found = True
		swap(West)
	
	return unsorted_found

def plant_cactus():
	plant(Entities.Cactus)

def create_task(startx, starty, width, height):
	def f():
		change_hat(Hats.Cactus_Hat)
		endx = startx+width - 1
		endy = starty+height - 1
		util.move_to(startx, starty)
		#setup_field(startx, starty, endx, endy)
		util.traverse_zig_zag(startx, starty, width, height, till)

		while True:
			util.traverse_zig_zag(startx, starty, width, height, plant_cactus)
			while True:
				unsorted_found = False
				def update():
					global unsorted_found
					if sort_north_south(get_pos_y(), starty, endy) or sort_east_west(get_pos_x(), startx, endx):
						unsorted_found = True
				util.traverse_zig_zag(startx, starty, width, height, update)
				if not unsorted_found:
					break
				#util.traverse_zig_zag(startx, starty, width, height, update, West, North)
				#if not unsorted_found:
					#break
			util.move_to(endx, endy)
			use_item(Items.Fertilizer)
			harvest()
	return f

def create_task_old(startx, starty, width, height):
	ws = get_world_size()
	def f():
		change_hat(Hats.Cactus_Hat)
		endx = startx+width
		endy = starty+height
		util.move_to(startx, starty)
		setup_field(startx, starty, endx, endy)

		while True:
			plant_field(startx, starty, endx, endy)
			while True:
				unsorted_found = False
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
						if y != endy - 1 and measure() > measure(North):
							unsorted_found = True
							swap(North)
						if x != endx - 1 and measure() > measure(East):
							unsorted_found = True
							swap(East)
				if not unsorted_found:
					break
			util.move_to(endx - 1, endy - 1)
			harvest()
	return f

if __name__ == "__main__":
	clear()
	set_world_size(16)
	create_task(2, 5, 12, 4)()