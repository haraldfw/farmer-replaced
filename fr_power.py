import util
import goals

def create_petal_list():
	petals = []
	for i in range(7, 16):
		petals.append([])
	return petals

def ensure_and_measure_watered_sunflower(petals):
	if get_ground_type() != Grounds.Soil:
		till()
	if get_entity_type() != Entities.Sunflower:
		harvest()
	plant(Entities.Sunflower)
	# first element are the ones to be harvested first
	measure_index = 15-measure()
	if measure_index < 2:
		util.water_to(0.75)
	petals[measure_index].append([get_pos_x(), get_pos_y()])

def single_drone_planting(petals, ws=get_world_size()):
	def f():
		global petals
		ensure_and_measure_watered_sunflower(petals)
	util.traverse_zig_zag_dynamic(ws, f)

def plant_and_measure_column(petals, columnx, dir, ws=get_world_size()):
	util.move_to_x(columnx)
	for i in range(ws):
		ensure_and_measure_watered_sunflower(petals)
		if i < ws - 1:
			# move on all iterations except last one
			move(North)
	return petals

def spawn_planting_drone(columnx, dir, ws=get_world_size()):
	def task():
		return plant_and_measure_column(create_petal_list(), columnx, dir, ws)
	handle = spawn_drone(task)
	return handle

def multi_drone_planting(petals, ws=get_world_size()):
	drones = []
	for columnx in range(ws):
		if columnx != ws-1 and num_drones() < max_drones() and columnx != ws -1:
			drone_handle = spawn_planting_drone(columnx, North, ws)
			if drone_handle:
				drones.append(drone_handle)
		else:
			plant_and_measure_column(petals, columnx, ws)
			for d in drones:
				new_petals = wait_for(d)
				for i in range(9):
					petals[i] += new_petals[i]
				drones = []
	

def single_drone_harvest(petals, ws, ws_squared):
	i = 0
	flowers_left = ws_squared
	for petal_coords in petals:
		if flowers_left <= 8:
			petals[i]=[]
			i+=1
			continue
		for coord in petal_coords:
			go_harvest(coord[0], coord[1], ws)
			flowers_left -= 1
			if flowers_left <= 8:
				util.move_to_closest_corner(ws)
				break
		petals[i]=[]
		i+=1

def go_harvest(x, y, ws):
	util.move_to(x, y, ws)
	while not can_harvest():
		util.water_to(0.75)

	harvest()

def create_harvest_task(x, y, ws):
	def f():
		go_harvest(x, y, ws)
	return f

def go_harvest_multiple(coords, ws):
	for coord in coords:
		x, y = coord
		go_harvest(x, y, ws)

def create_harvest_multiple_task(to_harvest, ws):
	def f():
		go_harvest_multiple(to_harvest, ws)
	return f

def deploy_harvest_drones_and_wait(to_harvest, ws):
	drones = []
	task_packets = {}
	mx_dr = max_drones()
	for i in range(len(to_harvest)):
		k = i % mx_dr
		if k not in task_packets:
			task_packets[k] = 1
		else:
			task_packets[k] += 1
	next_task_index = 0
	for i in range(len(task_packets)):
		num_tasks_to_take = task_packets[i]
		coords_to_harvest = to_harvest[next_task_index:next_task_index+num_tasks_to_take]
		if num_drones() < max_drones():
			next_task_index += num_tasks_to_take
			drones.append(spawn_drone(create_harvest_multiple_task(coords_to_harvest, ws)))
		else:
			next_task_index += num_tasks_to_take
			# last drone, do the task yourself
			go_harvest_multiple(coords_to_harvest, ws)
	for d in drones:
		wait_for(d)

def asdf():
	# ///
	tasks_per_drone = -1
	if tasks_left % max_drones() == 0:
		tasks_per_drone = tasks_left / max_drones()
	while tasks_left:
		if tasks_left == 1:
			x, y = to_harvest[next_task_index]
			go_harvest(x, y, ws)
			break
		if tasks_left <= tasks_per_drone:
			# 
			go_harvest_multiple(to_harvest[next_task_index:next_task_index+tasks_per_drone])
		
	for d in drones:
		wait_for(d)
			
	for coord in to_harvest:
		if num_drones() < max_drones():
			drones.append(spawn_drone(create_harvest_task(coord[0], coord[1], ws)))
		else:
			go_harvest(coord[0], coord[1], ws)
	for d in drones:
		wait_for(d)

def multi_drone_harvest(petals, ws, ws_squared):
	i = 0
	flowers_left = ws_squared
	for petal_coords in petals:
		if flowers_left <= 8:
			petals[i]=[]
			i+=1
			continue
		deploy_harvest_drones_and_wait(petal_coords, ws)
		flowers_left -= len(petal_coords)
		petals[i]=[]
		i+=1

def do_until_single(goal_func):
	ws = get_world_size()
	ws_squared = ws*ws
	petals = create_petal_list()

	while not goal_func():
		single_drone_planting(petals, ws)
		single_drone_harvest(petals, ws, ws_squared)
	util.move_to_closest_corner(ws)

def do_until_mega(goal_func):
	ws = get_world_size()
	ws_squared = ws*ws
	petals = create_petal_list()

	while not goal_func():
		multi_drone_planting(petals, ws)
		multi_drone_harvest(petals, ws, ws_squared)
	util.move_to_closest_corner(ws)
	

def do_until(goal_func):
	if max_drones() == 1:
		do_until_single(goal_func)
	else:
		do_until_mega(goal_func)
	util.move_to_closest_corner()

if __name__ == "__main__":
	clear()
	set_world_size(8)
	do_until(goals.create_goal(None, { Items.Power: num_items(Items.Power)+100000 }))
