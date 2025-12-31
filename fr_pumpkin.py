import util
import goals

ws = None
wsr = None

# the different modes supported:
# 1. od = one drone mode, where only one drone is used
# 2. sc = one column per drone mode, so our drone count is equal to our world size
# 3. mc = multiple columns per drone. where each drone handles more than one
# 		column and we have more than one drone, but the count is lower than our world size

def plant_pumpkin():
	if get_ground_type() != Grounds.Soil:
		till()
	if get_entity_type() != Entities.Pumpkin:
		harvest()
	plant(Entities.Pumpkin)

def plant_column(startx):
	util.move_to_x(startx)
	for i in wsr:
		plant_pumpkin()
		util.water_to(0.25)
		move(North)

def mend_deads(deads):
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

def plant_and_mend_multiple_columns(startx, columns):
	util.move_to_x(startx)
	for x in range(columns):
		for _ in wsr:
			plant_pumpkin()
			util.water_to(0.25)
			move(North)
		if x != columns - 1:
			move(East)
	
	util.move_to_x(startx)
	deads = []
	for x in range(columns):
		for i in wsr:
			while not can_harvest():
				if get_entity_type() == Entities.Dead_Pumpkin:
					harvest()
					plant(Entities.Pumpkin)
					util.water_to(0.75)
					deads.append((get_pos_x(), get_pos_y()))
					break
				else:
					util.water_to(0.75)
			move(North)
		if x != columns - 1:
			move(East)
	mend_deads(deads)

def spawn_mc_drone(startx, columns):
	def f():
		plant_and_mend_multiple_columns(startx, columns)
	return spawn_drone(f)

def spawn_sc_drone(columnx):
	def task():
		plant_column(columnx)
		return plant_and_mend_deads_on_column(columnx)
	handle = spawn_drone(task)
	return handle

def plant_and_mend_deads_on_column(columnx):
	deads = []
	util.move_to_x(columnx)
	plant_column(columnx)
	for i in wsr:
		while not can_harvest():
			if get_entity_type() == Entities.Dead_Pumpkin:
				harvest()
				plant(Entities.Pumpkin)
				util.water_to(0.75)
				deads.append((get_pos_x(), get_pos_y()))
				break
			else:
				util.water_to(0.75)
		move(North)
	mend_deads(deads)

def spawn_single_column_drone(columnx):
	def f():
		plant_and_mend_deads_on_column(columnx)
	return spawn_drone(f)

# takes for granted that we have enough drones to delegate one drone per column
def plant_and_mend_entire_field_sc():
	drones = []
	for columnx in wsr:
		if columnx != ws-1:
			drone_handle = spawn_single_column_drone(columnx)
			drones.append(drone_handle)
		else:
			# last drone, do this column yourself
			plant_and_mend_deads_on_column(columnx)
	for d in drones:
		wait_for(d)

def plant_and_mend_entire_field_od():
	util.traverse_l_pattern(plant_pumpkin, ws)
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
	util.traverse_l_pattern(find_and_replant_deads, ws)
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

def plant_and_mend_entire_field_mc():
	total_drones = max_drones()
	drones = []
	next_start_x = 0
	columns_left = ws
	while True:
		if total_drones == 1:
			plant_and_mend_multiple_columns(next_start_x, columns_left)
			break
		take_columns = util.ceil(columns_left/total_drones)
		drones.append(spawn_mc_drone(next_start_x, take_columns))
		next_start_x += take_columns
		columns_left -= take_columns
		total_drones -= 1

	for d in drones:
		wait_for(d)

def satisfy_cost(pumpkin_cost, _ws=get_world_size()):
	global ws
	global wsr
	ws = _ws
	wsr = range(ws)

	md = max_drones()
	if md >= ws:
		while num_items(Items.Pumpkin) < pumpkin_cost:
			plant_and_mend_entire_field_sc()
			harvest()
	elif md == 1:
		while num_items(Items.Pumpkin) < pumpkin_cost:
			plant_and_mend_entire_field_od()
			harvest()
	else:
		while num_items(Items.Pumpkin) < pumpkin_cost:
			plant_and_mend_entire_field_mc()
			harvest()

def satisfy_substance_cost(substance_cost, _ws=get_world_size()):
	global ws
	global wsr
	ws = _ws
	wsr = range(ws)

	md = max_drones()
	if md >= ws:
		while num_items(Items.Weird_Substance) < substance_cost:
			plant_and_mend_entire_field_sc()
			use_item(Items.Fertilizer)
			harvest()
	elif md == 1:
		while num_items(Items.Weird_Substance) < substance_cost:
			plant_and_mend_entire_field_od()
			use_item(Items.Fertilizer)
			harvest()
	else:
		while num_items(Items.Weird_Substance) < substance_cost:
			plant_and_mend_entire_field_mc()
			use_item(Items.Fertilizer)
			harvest()

if __name__ == "__main__":
#	clear()
#	set_world_size(32)
#	do_until(goals.create_goal(None, { Items.Pumpkin: num_items(Items.Pumpkin)+200000000 }))
	satisfy_cost(num_items(Items.Pumpkin)+200000000)

# TODO for leaderboard: do not let worker-drones exit after mending is finished. Instead
# wait for the main drone to harvest and then start replanting when there no longer is a
# pumpkin on their tile. This method might be able to be deployed when farming normally as well,
# but the worker drones then need to continually check for num_items > cost and then exit.
# for the main drone to figure out if the pumpkin is done `measure()` can be used.
# Measure returns the pumpkin's ID, so simply checking if two outer coordinates have the same
# return-value for `measure` lets you figure out if the field is grown or not. Simply make sure
# the main drone is on an edge, and measure, then move accross the edge and measure again,
# compare the values, if they are equal then harvest and restart. The main drones has to make
# sure that they are in the correct column before continuing on a new pumpkin.
# Worker drones only have to wait for their get_entity_type() to not be equal to Entities.Pumpkin

# An even better solution is to divide the field into squares instead of columns.
# This would let the drones travel way less when mending their part of the field.

# Doing any of these methods where the worker-drones live through multiple harvests, the main drone
# will have to call `clear()` before the next farm is started. This deletes all other drones.
