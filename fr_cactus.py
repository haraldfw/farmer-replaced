import util
import goals

ws = -1
end = -1

def plant_cactus():
	if get_ground_type() != Grounds.Soil:
		till()
	if get_entity_type() != Entities.Cactus:
		harvest()
	plant(Entities.Cactus)

def sort_column(columnx):
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

def sort_row(rowy):
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

def spawn_row_sorting_drone(rowy):
	def task():
		sort_row(rowy)
	handle = spawn_drone(task)
	return handle

def build_sorted_field_od():
	util.traverse_l_pattern(plant_cactus, ws)
	for columnx in range(ws):
		sort_column(columnx)
	for rowy in range(ws):
		sort_row(rowy)

def plant_and_sort_column(columnx):
	util.move_to_x(columnx)
	for i in range(ws):
		plant_cactus()
		if i < ws - 1:
			# do not move on last iteration
			move(North)
	
	sort_column(columnx)

def spawn_planting_drone(columnx):
	def task():
		plant_and_sort_column(columnx)
	return spawn_drone(task)

# multi-drone
def build_sorted_field_sc():
	global ws
	global end

	util.move_to_x(0, ws)
	drones = []
	for columnx in range(ws):
		if columnx != ws-1 and num_drones() < max_drones():
			drone_handle = spawn_planting_drone(columnx)
			if drone_handle:
				drones.append(drone_handle)
		else:
			plant_and_sort_column(columnx)
	while drones:
		wait_for(drones[0])
		drones.pop(0)

	for rowy in range(ws-1, -1, -1):
		if rowy != 0 and num_drones() < max_drones():
			drone_handle = spawn_row_sorting_drone(rowy)
			if drone_handle:
				drones.append(drone_handle)
		else:
			sort_row(rowy)

	util.move_to(end, end)
	while drones:
		wait_for(drones[0])
		drones.pop(0)

def satisfy_substance_cost_sc(substance_cost):
	global ws
	global end
	ws = get_world_size()
	end = ws-1

	while num_items(Items.Weird_Substance) < substance_cost:
		build_sorted_field_sc()
		use_item(Items.Fertilizer)
		harvest()

def satisfy_substance_cost_od(substance_cost):
	global ws
	global end

	ws = get_world_size()
	end = ws-1

	while num_items(Items.Weird_Substance) < substance_cost:
		build_sorted_field_od()
		util.move_to(end, end)
		use_item(Items.Fertilizer)
		harvest()

def satisfy_cost_sc(cactus_cost):
	global ws
	global end
	ws = get_world_size()
	end = ws-1

	while num_items(Items.Cactus) < cactus_cost:
		build_sorted_field_sc()
		harvest()

def satisfy_cost_od(cactus_cost):
	global ws
	global end

	ws = get_world_size()
	end = ws-1

	while num_items(Items.Cactus) < cactus_cost:
		build_sorted_field_od()
		util.move_to(end, end)
		harvest()

def satisfy_cost(cactus_cost):
	if num_unlocked(Unlocks.Megafarm) > 0:
		satisfy_cost_sc(cactus_cost)
	else:
		satisfy_cost_od(cactus_cost)

def satisfy_substance_cost(substance_cost):
	if num_unlocked(Unlocks.Megafarm) > 0:
		satisfy_substance_cost_sc(substancecost)
	else:
		satisfy_substance_cost_od(substance_cost)

if __name__ == "__main__":
	satisfy_cost(999999999999)

# TODO: figure out a way for drones to be able to complete an entire build without having to be
# respawned at any time. Since all cacti are harvested the drones can just wait until get_entity_type()
# returns None, so the main challenge is whether all columns have to be sorted before rows can be
# sorted.
