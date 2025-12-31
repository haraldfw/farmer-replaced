def move_to(goalx, goaly, ws=get_world_size(), posx=get_pos_x(), posy=get_pos_y()):
	move_to_x(goalx, ws, posx)
	move_to_y(goaly, ws, posy)

def move_to_x(goalx, ws=get_world_size(), posx=get_pos_x()):
	if goalx == posx:
		return True
	direct_distance = abs(goalx - posx)
	if direct_distance <= ws/2:
		dir = East
		if goalx < posx:
			dir = West
	else:
		dir = West
		if goalx < posx:
			dir = East
	pass
	while get_pos_x() != goalx:
		if not move(dir):
			return False
	return True

def move_to_y(goaly, ws=get_world_size(), posy=get_pos_y()):
	if goaly == posy:
		return True
	direct_distance = abs(goaly - posy)
	if direct_distance <= ws/2:
		dir = North
		if goaly < posy:
			dir = South
	else:
		dir = South
		if goaly < posy:
			dir = North
	while get_pos_y() != goaly:
		if not move(dir):
			return False
	return True

def water_to_max(water_val=get_water()):
	water_to(0.75, water_val)

def water_to(val, water_val=get_water()):
	if num_items(Items.Water) > 3 and water_val < val:
		use_item(Items.Water, (val + 0.25 - water_val)//0.25)

def ensure_ground(ground):
	if get_ground_type() != ground:
		till()

def ensure_plant(p):
	if get_entity_type() != p:
		plant(p)

def flip_direction(dir):
	if dir == North:
		return South
	if dir == South:
		return North
	if dir == West:
		return East
	if dir == East:
		return West

def rotate_cw(dir):
	if dir == North:
		return East
	if dir == South:
		return West
	if dir == West:
		return North
	if dir == East:
		return South

def rotate_ccw(dir):
	if dir == North:
		return West
	if dir == South:
		return East
	if dir == West:
		return South
	if dir == East:
		return North
	
def traverse_zig_zag(x, y, width, height, func, primary_dir=East, secondary_dir=North):
	primary_dimension = width
	secondary_dimension = height
	if primary_dir == North or primary_dir == South:
		primary_dimension = height
		secondary_dimension = width
	startx, starty = x, y
	if primary_dir == West:
		startx = x + width

	if secondary_dir == South:
		starty = y + height

	move_to(startx, starty)

	last_i = primary_dimension - 1
	last_j = secondary_dimension - 1
	for i in range(primary_dimension):
		for j in range(secondary_dimension):
			func()
			if j != last_j:
				move(secondary_dir)
		if i != last_i:
			move(primary_dir)
		secondary_dir = flip_direction(secondary_dir)
	
# takes for granted that we start in our required location, directions pointing away
def traverse_zig_zag_naive(x, y, width, height, func, primary_dir=East, secondary_dir=North):
	primary_dimension = width
	secondary_dimension = height
	if primary_dir == North or primary_dir == South:
		primary_dimension = height
		secondary_dimension = width

	last_i = primary_dimension - 1
	last_j = secondary_dimension - 1
	for i in range(primary_dimension):
		for j in range(secondary_dimension):
			func()
			if j != last_j:
				move(secondary_dir)
		if i != last_i:
			move(primary_dir)
		secondary_dir = flip_direction(secondary_dir)

# takes for granted that we are at a corner
def traverse_zig_zag_dynamic(world_size, func):
	x = get_pos_x()
	y = get_pos_y()
	end = world_size-1
	# x == 0 and y == 0:
	dir = East
	secondary_dir = North
	if x == end and y == 0:
		dir = North
		secondary_dir = West
	elif x == end and y == end:
		dir = West
		secondary_dir = South
	elif x == 0 and y == end:
		dir = South
		secondary_dir = East
	traverse_zig_zag_naive(x, y, world_size, world_size, func, dir, secondary_dir)

def traverse_l_pattern(func, ws=get_world_size(), extra_move_at_end=False):
	end = ws - 1
	wsr = range(ws)
	for i in wsr:
		for j in wsr:
			func()
			if j == end:
				move(East)
			else:
				move(North)


def move_to_closest_corner(ws=get_world_size()):
	end = ws-1
	x = get_pos_x()
	y = get_pos_y()
	if (x == 0 or x == end) and (y == 0 or y == end):
		return
	mid = end/2
	if x < mid:
		move_to_x(0)
	else:
		move_to_x(end)
	if y < mid:
		move_to_y(0)
	else:
		move_to_y(end)

def move_over_any_edge(ws=get_world_size()):
	x = get_pos_x()
	if x == 0:
		move(West)
		return
	y = get_pos_y()
	if y == 0:
		move(South)
		return
	end = ws-1
	if x == end:
		move(East)
		return
	if y == end:
		move(North)
		return
	assert() # fails

def move_over_edge_x(ws=get_world_size()):
	x = get_pos_x()
	if x == 0:
		move(West)
		return
	end = ws-1
	if x == end:
		move(East)
		return
	assert() # fails

def move_over_edge_y(ws=get_world_size()):
	y = get_pos_y()
	if y == 0:
		move(South)
		return
	end = ws-1
	if y == end:
		move(North)
		return
	assert() # fails

def ceil(num):
	if num % 1 == 0:
		return num
	return (num // 1) + 1

costs = {
	Items.Pumpkin: {
		Items.Carrot: 1
	},
	Items.Cactus: {
		Items.Pumpkin: 2
	},
	Items.Carrot: {
		Items.Hay: 1,
		Items.Wood: 1
	},
	Items.Bone: {
		Items.Cactus: 2
	},
}

# NOT DONE
def calc_costs(requirements, ws=get_world_size()):
	task_list = []
	while requirements:
		for key in requirements:
			cost = requirements.pop(key)
			new_req[key] = cost
			if key == Items.Weird_Substance:
				pass
			elif key in costs:
				other_reqs = asdf
	for req_item in requiremements:
		cost = requirements[req_item]
		if req_item == Items.Bone:
			pass
		elif req_item == Items.Cactus:
			new_req[Items.Pumpkin] = cost*2
		elif req_item == Items.Carrot:
			new_req[Items.Hay] = cost
			new_req[Items.Wood] = cost
	return new_req

if __name__ == "__main__":
	set_world_size(5)
	clear()
	ws = get_world_size()
	move_to(2, 4)
	#traverse_zig_zag_dynamic(get_world_size(), get_pos_x)
	#traverse_zig_zag_dynamic(get_world_size(), get_pos_x)
	#traverse_zig_zag_dynamic(get_world_size(), get_pos_x)
	#traverse_zig_zag_dynamic(get_world_size(), get_pos_x)
	# move_to(ws-1, ws-1)
	
	# move_to(ws//4, ws//4)
	# move_to(0, 0)
	# move_to(ws-1, ws-1)
	# move_to(ws//4, ws//4)
	set_execution_speed(1)
	traverse_l_pattern(get_pos_y, ws, True)
	while True:
		continue
