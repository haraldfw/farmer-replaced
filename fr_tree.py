import util
import goals

def tile_operation():
	util.traverse_zig_zag_dynamic()

def do_until(goal_func):
	plants = [Entities.Grass, Entities.Carrot, Entities.Tree]
	ws = get_world_size()

	def handle_tile():
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
				elif to_plant == Entities.Tree:
					util.water_to(0.5)
				plant(to_plant)
	while not goal_func():
		util.traverse_l_pattern(handle_tile, ws)

if __name__ == "__main__":
	clear()
	set_world_size(8)
	do_until(goals.infinite_goal)
