import util
import goals

plants = [Entities.Grass, Entities.Carrot, Entities.Tree]
ws = -1
companions = None

def plant_grass():
	if can_harvest():
		harvest()
	if get_ground_type() != Grounds.Grassland:
		till()

def plant_tree():
	if can_harvest():
		harvest()
	plant(Entities.Tree)


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

def handle_tile():
	global requests
	attempt_harvest_and_update_companions()
	pos = (get_pos_x(), get_pos_y())
	tile_num = pos[0]+pos[1]
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

def satisfy_costs(hay_cost, wood_cost, carrot_cost):
	global ws
	global companions


	ws = get_world_size()
	companions={}

	tile_num = 0

	while num_items(Items.Hay) < hay_cost:
		util.traverse_l_pattern(handle_tile, ws)
	while num_items(Items.Wood) < wood_cost:
		util.traverse_l_pattern(handle_tile, ws)
	while num_items(Items.Carrot) < carrot_cost:
		util.traverse_l_pattern(handle_tile, ws)

if __name__ == "__main__":
	clear()
	set_world_size(8)
	satisfy_costs(999999999999, 999999999999, 999999999999)
