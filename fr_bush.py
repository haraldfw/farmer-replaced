import util
import goals

def do_until_single_lane(goal_func):
	while not goal_func():
		if can_harvest():
			harvest()
			plant(Entities.Bush)
		move(North)

def do_until_multi_lane(goal_func):
	moves = 0
	while not goal_func():
		if can_harvest():
			harvest()
			plant(Entities.Bush)
		if moves % 3 == 0:
			move(East)
		else:
			move(North)
		moves += 1

if __name__ == "__main__":
	set_world_size(3)
	set_execution_speed(1)
	do_multi_lane(goals.infinite_goal)
