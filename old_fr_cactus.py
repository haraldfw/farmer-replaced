import util
import goals

def sort_column_until_sorted(columnx, ws=get_world_size()):
	end = ws - 2
	starty = 1
	dir = North
	if goaly > end/2:
		dir = South
		starty = end - 1
	util.move_to(columnx, goaly, ws)

	unsorted_found = False
	# populate array
	arr = []
	if y == starty:
		arr.append(measure(South))
		for _ in range(ws - 3):
			arr.append(measure())
			move(North)
		arr.append(measure(North))

	dir = util.flip_direction(dir)
	while True:
		y = get_pos_y()
		# every time we reach an end of the column, flip direction and check for sorted
		if y == starty or y == end:
			if not unsorted_found:
				break
			unsorted_found = False
			dir = util.flip_direction(dir)
		if sort_north_south(y, 0, end):
			unsorted_found = True
		move(dir)

def sort_row_until_sorted(rowy, end=get_world_size()-1):
	goalx = 0
	dir = East
	if goalx > end/2:
		dir = West
		goalx = end
	util.move_to(goalx, rowy, ws)
	
	unsorted_found = False
	while True:
		x = get_pos_x()
		# flip direction and check for sort on ends of column
		if x == 0 or x == end:
			if not unsorted_found:
				break
			unsorted_found = False
			dir = util.flip_direction(dir)
		sort_north_south(y, 0, end)
		move(dir)

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
	if get_ground_type() != Grounds.Soil:
		till()
	if get_entity_type() != Entities.Cactus:
		harvest()
	plant(Entities.Cactus)

def do_until(goal_func):
	ws = get_world_size()
	end = ws-1

	unsorted_found = False
	def attempt_sort():
		global unsorted_found
		if sort_north_south(get_pos_y(), 0, end) or sort_east_west(get_pos_x(), 0, end):
			unsorted_found = True

	while not goal_func():
		util.traverse_zig_zag_dynamic(ws, plant_cactus)
		while True:
			unsorted_found = False
			util.traverse_zig_zag_dynamic(ws, attempt_sort)
			if not unsorted_found:
				break
			#util.traverse_zig_zag(startx, starty, width, height, update, West, North)
			#if not unsorted_found:
				#break
		util.move_to(end, end)
		if num_items(Items.Fertilizer) > 0:
			use_item(Items.Fertilizer)
		harvest()

if __name__ == "__main__":
	clear()
	set_world_size(8)
	do_until(goals.create_goal(None, { Items.Cactus: num_items(Items.Cactus)+2000000 }))
