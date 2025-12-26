import util
import goals

def plant_pumpkin():
	if get_ground_type() != Grounds.Soil:
		till()
	if get_entity_type() != Entities.Pumpkin:
		harvest()
	plant(Entities.Pumpkin)

def do_until(goal_func):
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
						if num_items(Items.Fertilizer) > 0:
							use_item(Items.Fertilizer)
						break
				deads.pop(i)
		harvest()
		util.move_to_closest_corner(ws)

if __name__ == "__main__":
	clear()
	set_world_size(32)
	do_until(goals.infinite_goal)
