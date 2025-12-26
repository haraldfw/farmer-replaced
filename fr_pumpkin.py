import util

def plant_pumpkin():
	if get_ground_type() != Grounds.Soil:
		till()
	if get_entity_type() != Entities.Pumpkin:
		harvest()
	plant(Entities.Pumpkin)

def plant_column(columnx, dir, ws=get_world_size()):
	util.move_to_x(columnx)
	for i in range(ws):
		plant_pumpkin()
		if i < ws - 1:
			# do not move on last iteration
			move(North)

def spawn_planting_drone(columnx, dir, ws=get_world_size()):
	def task():
		plant_column(columnx, dir, ws)
	handle = spawn_drone(task)
	return handle

def plant_field_multi(ws=get_world_size()):
	drones = []
	for columnx in range(ws):
		if columnx != ws-1 and num_drones() < max_drones():
			drone_handle = spawn_planting_drone(columnx, North, ws)
			drones.append(drone_handle)
		else:
			plant_column(columnx, ws)
	for d in drones:
		wait_for(d)

def find_deads_on_column(columnx, ws=get_world_size()):
	deads = []
	util.move_to_x(columnx)
	for i in range(ws):
		while not can_harvest():
			if get_entity_type() == Entities.Dead_Pumpkin:
				harvest()
				plant(Entities.Pumpkin)
				util.water_to(0.75)
				deads.append((get_pos_x(), get_pos_y()))
				break
			else:
				util.water_to(0.75)
		if i != ws - 1:
			move(North)
	return deads

def spawn_deads_finding_drone(columnx, ws=get_world_size()):
	def f():
		return find_deads_on_column(columnx, ws)
	return spawn_drone(f)

def find_deads_multi(ws=get_world_size()):
	deads = []
	drones = []
	for columnx in range(ws):
		if columnx != ws-1 and num_drones() < max_drones():
			drone_handle = spawn_deads_finding_drone(columnx, ws)
			drones.append(drone_handle)
		else:
			deads += find_deads_on_column(columnx, ws)
	for d in drones:
		deads += wait_for(d)
	return deads

def mend_deads_multi(deads, ws=get_world_size()):
	drones = []
	task_packets = {}
	mx_dr = max_drones()
	for i in range(len(deads)):
		k = i % mx_dr
		if k not in task_packets:
			task_packets[k] = 1
		else:
			task_packets[k] += 1
	next_task_index = 0
	for i in range(len(task_packets)):
		num_tasks_to_take = task_packets[i]
		coords_to_mend = deads[next_task_index:next_task_index+num_tasks_to_take]
		if num_drones() < max_drones() and i < len(task_packets) - 1:
			next_task_index += num_tasks_to_take
			drones.append(spawn_mend_multiple_drone(coords_to_mend, ws))
		else:
			next_task_index += num_tasks_to_take
			# last drone, do the task yourself
			mend_deads(coords_to_mend, ws)
	for d in drones:
		wait_for(d)

def mend_deads(deads, ws):
	while deads:
		i = 0
		for _ in range(len(deads)):
			deadx, deady = deads[i]
			util.move_to(deadx, deady)
			pop_it = True
			while not can_harvest():
				util.water_to(0.75)
				if get_entity_type() == Entities.Dead_Pumpkin:
					harvest()
					plant(Entities.Pumpkin)
					pop_it = False
					break
			if pop_it:
				deads.pop(i)
			else:
				i += 1
				
			

def spawn_mend_multiple_drone(deads, ws):
	def f():
		mend_deads(deads, ws)
	return spawn_drone(f)

def do_until_multi(goal_func):
	while not goal_func():
		ws = get_world_size()
		plant_field_multi(ws)
		deads = find_deads_multi(ws)
		mend_deads_multi(deads, ws)
		harvest()

def do_until_single(goal_func):
	ws = get_world_size()

	while not goal_func():
		util.move_to_closest_corner(ws)
		util.traverse_zig_zag_dynamic(ws, plant_pumpkin)
		# move to other corner to let the one we are standing on grow
		util.move_over_edge_x(ws)
		util.move_over_edge_y(ws)
		deads = []
		def find_and_replant_deads():
			global deads
			while not can_harvest():
				util.water_to(0.5)
				if get_entity_type() == Entities.Dead_Pumpkin:
					harvest()
					plant(Entities.Pumpkin)
					util.water_to(0.5)
					deads.append((get_pos_x(), get_pos_y()))
					return
		util.traverse_zig_zag_dynamic(ws, find_and_replant_deads)
		while deads:
			i = 0
			for _ in range(len(deads)):
				deadx, deady = deads[i]
				util.move_to(deadx, deady)
				while not can_harvest():
					if get_entity_type() == Entities.Dead_Pumpkin:
						harvest()
						plant(Entities.Pumpkin)
						util.water_to(0.5)
						deads.append((get_pos_x(), get_pos_y()))
						break
				deads.pop(i)
		harvest()
		util.move_to_closest_corner(ws)

def do_until(goal_func):
	if max_drones() == 1:
		do_until_single(goal_func)
	else:
		do_until_multi(goal_func)

if __name__ == "__main__":
	clear()
	set_world_size(32)
	do_until(util.create_goal(None, { Items.Pumpkin: num_items(Items.Pumpkin)+200000000 }))