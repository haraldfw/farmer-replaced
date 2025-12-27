import util
import goals

# where a drone should start if it wans to use the lap solution
start_x, start_y = -1, -1
# what moves to execute from the start x and y to do an entire lap of the original map
lap_moves = []
# list of drones currently lapping to map out the world
mappers = []

# graph of the world map
# a node record looks like this: 
world_map =	{}

dirs = [North, East, South, West]

def spawn_mapper():
	def f():
		x, y = get_pos_x(), get_pos_y()
		to_start_moves = find_solution

def update_mappers():
	if mappers and has_finished(mappers[0]):
		map_graph = wait_for(mappers.pop(0))
		

def rotate_ccw(index):
	return (index - 1) % 4

def rotate_cw(index):
	return (index + 1) % 4

def ensure_bush():
	if get_ground_type() != Grounds.Grassland:
		harvest()
		till()
	if get_entity_type() != Entities.Bush:
		plant(Entities.Bush)

def use_substance():
	substance_amount = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
	return use_item(Items.Weird_Substance, substance_amount)


def create_map_dict(world_size):
	m = {}
	for x in range(world_size):
		for y in range(world_size):
			m[(x, y)] = []
	return m

def get_heuristic(start, goal):
	# manhattan distance
	return (abs(goal[0]-start[0]) + abs(goal[1]-start[1]))

def get_location_in_direction(start, dir):
	x, y = start
	if dir == North:
		return (x, y+1)
	if dir == East:
		return (x+1, y)
	if dir == South:
		return (x, y-1)
	if dir == West:
		return (x-1, y)
	asdf()
	print("erroneous dir in get_location_in_direction")

def get_smallest_record(nodes):
	smallest_cost = 99999999
	smallest_rec = []
	for loc in nodes:
		nodeRecord = nodes[loc]
		estimatedTotalCost = nodeRecord[3]
		if estimatedTotalCost < smallest_cost: # estimatedTotalCost
			smallest_rec = nodeRecord
			smallest_cost = estimatedTotalCost
	return smallest_rec

# returns a list of moves to execute to end up on the wanted coordinates, using the drone's current
# position as the start
def find_solution(goal):
	# A-Star implementation
	# [
	#   (x, y),
	#   direction,
	#   costSoFar,
	#   estimatedTotalCost,
	#   cost
	# ]
	start = (get_pos_x(), get_pos_y())
	open_records = { start: [ start, None, 0, get_heuristic(start, goal), 0 ] } 
	closed_records = {}
	while open_records:
		currentRec = get_smallest_record(open_records)
		currLoc = currentRec[0]
		if currLoc == goal:
			# we have found our goal
			break
		# iterate connections
		for dir in world_map[currLoc]:
			# overwritten in all branches of nest if-statement
			endNodeHeuristic = 0

			endLoc = get_location_in_direction(currLoc, dir)

			# all connection costs are 1 in a tile grid
			# endNode.costSoFar + connectionCost
			endCost = currentRec[2] + 1

			if endLoc in closed_records:
				endRec = closed_records[endLoc]
				# if the path we found was not shorter, skip
				if endRec[2] <= endCost:
					continue
				# otherwise, remove from closed
				closed_records.pop(endLoc)
				endNodeHeuristic = endRec[3] - endRec[2]
			elif endLoc in open_records:
				endRec = open_records[endLoc]
				# if the path we found was not shorter, skip
				if endRec[2] <= endCost:
					continue
				endNodeHeuristic = endRec[4] - endRec[2]
			else:
				# unvisited node
				endRec = [
					endLoc,
					None,
					0,
					0,
					0
				]
				endNodeHeuristic = get_heuristic(endLoc, goal)

			endRec[1] = util.flip_direction(dir) # direction back to curr
			endRec[3] = endCost + endNodeHeuristic # estimatedTotalCost
			endRec[4] = endCost # cost
			if endLoc not in open_records:
				open_records[endLoc] = endRec

		open_records.pop(currLoc)
		closed_records[currLoc] = currentRec
	if currentRec[0] != goal:
		return None
	# we have found a path, we got'em
	solution = []
	while currLoc != start:
		solution.append(currentRec[1])
		currentRec = closed_records[get_location_in_direction(currLoc, currentRec[1])]
		currLoc = currentRec[0]
	
	reversed_solution = []
	for i in range(len(solution), 0, -1):
		reversed_solution.append(util.flip_direction(solution[i-1]))
	return reversed_solution

def reuse_maze():
	world_size = get_world_size()
	ensure_bush()
	use_substance()
	# { (x, y): [open directions, North, South]}
	#world_map = {} # create_map_dict(world_size)

	# traverse the entire map
	index = 0
	tiles_left_to_populated = world_size*world_size
	while tiles_left_to_populated > 0:
		pos = (get_pos_x(), get_pos_y())
		if pos not in world_map:
			# store valid directions from current tile
			valid_dirs = []
			if can_move(North):
				valid_dirs.append(North)
			if can_move(East):
				valid_dirs.append(East)
			if can_move(South):
				valid_dirs.append(South)
			if can_move(West):
				valid_dirs.append(West)
			world_map[pos] = valid_dirs
			tiles_left_to_populated -= 1

		dir = dirs[rotate_ccw(index)]
		if move(dir):
			index = rotate_ccw(index)
		elif not move(dirs[index]):
			index = rotate_cw(index)
		
	# map populated
	while True:
		treasurex, treasurey = measure()
		solution_moves = find_solution((treasurex, treasurey))
		for dir in solution_moves:
			pos = (get_pos_x(), get_pos_y())
			valid_dirs = []
			if can_move(North):
				valid_dirs.append(North)
			if can_move(East):
				valid_dirs.append(East)
			if can_move(South):
				valid_dirs.append(South)
			if can_move(West):
				valid_dirs.append(West)
			# update the map with new missing walls as we go
			world_map[pos] = valid_dirs
			move(dir)
		# path followed and we are standing over the treasure
		if not use_substance():
			# unable to use substance because this is the last chest (nr 300)
			harvest()
			return

def do_until(goal_func):
	while not goal_func():
		reuse_maze()

if __name__ == "__main__":
	clear()
	while True:
		set_world_size(8)
		do_until(goals.infinite_goal)
