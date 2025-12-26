import util
import goals

def plant_cactus():
	if get_ground_type() != Grounds.Soil:
		till()
	if get_entity_type() != Entities.Cactus:
		harvest()
	plant(Entities.Cactus)

def sort_column(columnx, ws=get_world_size()):
	util.move_to(columnx, 0)
	moves = ws - 2

	swapped = True
	while swapped:
		swapped = False
		for _ in range(moves):
			if measure() > measure(North):
				swap(North)
				swapped = True
			move(North)
		if measure() > measure(North):
			swap(North)
			swapped = True

		if not swapped:
			break

		swapped = False
		moves -= 1

		for _ in range(moves):
			if measure() < measure(South):
				swap(South)
				swapped = True
			move(South)
		if measure() < measure(South):
			swap(South)
			swapped = True

		moves -= 1

def sort_row(rowy, ws=get_world_size()):
	util.move_to(0, rowy)
	moves = ws - 2

	swapped = True
	while swapped:
		swapped = False
		for _ in range(moves):
			if measure() > measure(East):
				swap(East)
				swapped = True
			move(East)
		if measure() > measure(East):
			swap(East)
			swapped = True

		if not swapped:
			break

		swapped = False
		moves -= 1

		for _ in range(moves):
			if measure() < measure(West):
				swap(West)
				swapped = True
			move(West)
		if measure() < measure(West):
			swap(West)
			swapped = True

		moves -= 1

def spawn_sorting_drone(func, arg1, arg2):
	def task():
		func(arg1, arg2)
	handle = spawn_drone(task)
	return handle


def do_until_single(goal_func):
	ws = get_world_size()
	end = ws-1
	util.move_to(0, 0)

	unsorted_found = False
	arr = {}

	while not goal_func():
		util.traverse_zig_zag_dynamic(ws, plant_cactus)

		for columnx in range(ws):
			sort_column(columnx, ws)
		for rowy in range(ws):
			sort_row(rowy, ws)

		util.move_to(end, end)
		if num_items(Items.Fertilizer) > 0:
			use_item(Items.Fertilizer)
		harvest()

def plant_column(columnx, dir, ws=get_world_size()):
	util.move_to_x(columnx)
	for i in range(ws):
		plant_cactus()
		if i < ws - 1:
			# do not move on last iteration
			move(North)

def spawn_planting_drone(columnx, dir, ws=get_world_size()):
	def task():
		plant_column(columnx, dir, ws)
	handle = spawn_drone(task)
	return handle


def do_until_mega(goal_func):
	ws = get_world_size()
	end = ws-1
	util.move_to(0, 0)

	unsorted_found = False
	
	while not goal_func():
		util.move_to_x(0, ws)
		drones = []
		for columnx in range(ws):
			if columnx != ws-1 and num_drones() < max_drones():
				drone_handle = spawn_planting_drone(columnx, North, ws)
				if drone_handle:
					drones.append(drone_handle)
			else:
				plant_column(columnx, ws)
		while drones:
			wait_for(drones[0])
			drones.pop(0)

		drones = []
		for columnx in range(ws-1, -1, -1):
			if columnx != 0 and num_drones() < max_drones():
				drone_handle = spawn_sorting_drone(sort_column, columnx, ws)
				if drone_handle:
					drones.append(drone_handle)
			else:
				sort_column(columnx, ws)
		while drones:
			wait_for(drones[0])
			drones.pop(0)

		for rowy in range(ws-1, -1, -1):
			if rowy != 0 and num_drones() < max_drones():
				drone_handle = spawn_sorting_drone(sort_row, rowy, ws)
				if drone_handle:
					drones.append(drone_handle)
			else:
				sort_row(rowy, ws)

		util.move_to(end, end)
		while drones:
			wait_for(drones[0])
			drones.pop(0)
		harvest()

def do_until(goal_func):
	if num_unlocked(Unlocks.Megafarm) > 0:
		do_until_mega(goal_func)
		#do_until_mega(goal_func)
	else:
		do_until_single(goal_func)

if __name__ == "__main__":
	clear()
	set_world_size(32)
	do_until(goals.create_goal(None, { Items.Cactus: num_items(Items.Cactus)+20000000 }))
