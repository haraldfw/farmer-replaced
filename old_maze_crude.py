import util

dirs = [North, East, South, West]

def ensure_bush():
	if get_ground_type() != Grounds.Grassland:
		harvest()
		till()
	if get_entity_type() != Entities.Bush:
		plant(Entities.Bush)

def create_maze():
	substance_amount = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance_amount)

def rotate_ccw(index):
	return (index - 1) % 4

def rotate_cw(index):
	return (index + 1) % 4

def solve_right_first():
	index = 1
	while True:
		if get_entity_type() == Entities.Grass or get_entity_type() == Entities.Treasure:
			harvest()
			break
		# if we were able to move right
		if move(dirs[rotate_cw(index)]):
			# turn direction to right
			index = rotate_cw(index)
		elif not move(dirs[index]):
			index = rotate_ccw(index)

def run_single_maze_solve():
	if get_entity_type() != Entities.Hedge:
		ensure_bush()
		create_maze()
	spawn_drone(solve_right_first)
	index = 0
	while True:
		if get_entity_type() == Entities.Grass or get_entity_type() == Entities.Treasure:
			harvest()
			break
		if move(dirs[rotate_ccw(index)]):
			index = rotate_ccw(index)
		elif not move(dirs[index]):
			index = rotate_cw(index)

if __name__ == "__main__":
	while True:
		run_single_maze_solve()
