import util
import goals

def harvest_and_ensure_bush():
	if can_harvest():
		harvest()
		plant(Entities.Bush)

def satisfy_cost_single_lane(wood_cost):
	while num_items(Items.Wood) < wood_cost:
		if can_harvest():
			harvest()
			plant(Entities.Bush)
		move(North)

def satisfy_cost_multi_lane(wood_cost):
	while num_items(Items.Wood) < wood_cost:
		util.traverse_l_pattern(harvest_and_ensure_bush, ws)

def satisfy_cost(wood_cost, _ws=get_world_size()):
	global ws
	ws = _ws
	if ws == 1:
		satisfy_cost_single_lane(wood_cost)
	else:
		satisfy_cost_multi_lane(wood_cost)
		
if __name__ == "__main__":
	set_world_size(3)
	set_execution_speed(3)
	do_until_multi_lane(goals.infinite_goal)
