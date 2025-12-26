import util
import goals

plants = [Entities.Grass, Entities.Carrot, Entities.Tree]

def plant_grass():
	if can_harvest():
		harvest()
	if get_ground_type() != Grounds.Grassland:
		till()

def plant_tree():
	if can_harvest():
		harvest()
	plant(Entities.Tree)

def do_until(goal_func):
	ws = get_world_size()
	companions={}
	loop_dir = East
	end = ws-1
	x, y = get_pos_x(), get_pos_y()
	if x == end and y == 0:
		loop_dir = North
	elif x == 0 and y == end:
		loop_dir = South
	elif x == end and y == end:
		loop_dir = East

	def attempt_harvest_and_update_companions():
		global companions
		if not can_harvest():
			return False
		_, comp_pos = get_companion()
		# if this plant has a defined companion, then we can remove it because we are harvesting it
		if comp_pos in companions:
			#quick_print("companion predefined, possibly harvesting with bonus")
			companions.pop(comp_pos)
		#else:
			#quick_print("companion NOT defined, harvesting without bonus")
		# always True
		return harvest()

	def plant_and_update_companions(to_plant):
		if to_plant == Entities.Grass:
			if get_ground_type() != Grounds.Grassland:
				till()
		else:
			if to_plant == Entities.Carrot and get_ground_type() != Grounds.Soil:
				till()
			elif to_plant == Entities.Tree:
				util.water_to_max()
			plant(to_plant)
		
		comp, comp_pos = get_companion()
		companions[comp_pos] = comp

	tile_num = 0
	def f():
		global requests
		global tile_num
		tile_num += 1
		attempt_harvest_and_update_companions()
		pos = (get_pos_x(), get_pos_y())
		plant_requested = False
		planted = get_entity_type()
		# if the plant planted is a companion, harvest and replant the same plant
		# do some checks to do specific tasks
		if pos in companions:
			comp = companions[pos]
			attempt_harvest_and_update_companions()
			plant_and_update_companions(comp)
			return

		to_plant = plants[tile_num % 3]
		attempt_harvest_and_update_companions()
		plant_and_update_companions(to_plant)
		return
		# if a companion is requested, then overplant anything present
		if planted != to_plant and (plant_requested or planted == None or planted == Entities.Grass):
			if to_plant == Entities.Grass:
				if comp_pos in companions:
					companions.pop(comp_pos)
				harvest()
				if get_ground_type() != Grounds.Grassland:
					till()
				comp, comp_pos = get_companion()
				companions[comp_pos] = comp
			elif to_plant == Entities.Carrot:
				harvest()
				if get_ground_type() != Grounds.Soil:
					till()
				plant(Entities.Carrot)
				comp, comp_pos = get_companion()
				companions[comp_pos] = comp
			elif to_plant == Entities.Tree:
				harvest()
				plant(Entities.Tree)
				util.water_to_max()
				comp, comp_pos = get_companion()
				companions[comp_pos] = comp
			elif to_plant == Entities.Bush:
				harvest()
				plant(Entities.Bush)
				comp, comp_pos = get_companion()
				companions[comp_pos] = comp
	while not goal_func():
		util.traverse_zig_zag(0, 0, ws, ws, f)
		move(loop_dir)

if __name__ == "__main__":
	clear()
	set_world_size(8)
	do_until(goals.infinite_goal)
