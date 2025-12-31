import util
import goals

def satisfy_costs(hay_cost, wood_cost, carrot_cost):
	plants = [Entities.Grass, Entities.Carrot, Entities.Bush]
	ws = get_world_size()
	tile_num = 0

	def handle_tile():
		global tile_num
		if can_harvest():
			harvest()

		to_plant = plants[(get_pos_y()+get_pos_x()) % 3]
		if get_entity_type() != to_plant:
			if to_plant == Entities.Grass:
				if get_ground_type() != Grounds.Grassland:
					till()
			else:
				if to_plant == Entities.Carrot and get_ground_type() != Grounds.Soil:
					till()
				plant(to_plant)
		tile_num+=1

	while num_items(Items.Hay) < hay_cost:
		util.traverse_l_pattern(handle_tile, ws)
	while num_items(Items.Wood) < wood_cost:
		util.traverse_l_pattern(handle_tile, ws)
	while num_items(Items.Carrot) < carrot_cost:
		util.traverse_l_pattern(handle_tile, ws)

if __name__ == "__main__":
	clear()
	set_world_size(8)
	do_until(goals.infinite_goal)
