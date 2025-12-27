import util
import goals

def tile_operation():
	util.traverse_zig_zag_dynamic()

def do_until(goal_func):
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
	while not goal_func():
		util.traverse_l_pattern(handle_tile, ws)

if __name__ == "__main__":
	clear()
	set_world_size(8)
	do_until(goals.infinite_goal)
