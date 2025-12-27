import util
import goals

def harvest_and_ensure_bush():
	if can_harvest():
		harvest()
		plant(Entities.Bush)
	

def do_until_single_lane(goal_func):
	while not goal_func():
		if can_harvest():
			harvest()
			plant(Entities.Bush)
		move(North)

def do_until_multi_lane(goal_func, ws=get_world_size()):
	while not goal_func():
		util.traverse_l_pattern(harvest_and_ensure_bush)
		
if __name__ == "__main__":
	set_world_size(3)
	set_execution_speed(3)
	do_until_multi_lane(goals.infinite_goal)
