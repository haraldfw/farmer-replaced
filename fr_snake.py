import util
import goals

ws, end, top_line_y, bottom_line_y, detour_length = -1,-1,-1,-1, -1
snake_length = 1
applex, appley = -1, -1
x, y = -1, -1
detours_needed_per_lap = 0
length_for_almighty = -1
almighty = False

def update_detours():
	global detours_needed_per_lap
	global almighty
	if not almighty:
		extra_length = snake_length - ws * 2
		detours_needed_per_lap = max(0, extra_length/(detour_length*2-2))
		if snake_length > length_for_almighty:
			almighty = True
	

def measure_and_move(dir, times):
	global applex
	global appley
	global detours_needed_per_lap
	global snake_length
	for _ in range(times):
		if get_entity_type() == Entities.Apple:
			applex, appley = measure()
			snake_length += 1
			update_detours()
		if not move(dir):
			return False
	return True


def do_detour(dir, length):
	if not measure_and_move(dir, length):
		return False
	if not measure_and_move(util.rotate_cw(dir), 1):
		return False
	if not measure_and_move(util.flip_direction(dir), length):
		return False
	return True

def do_full_board():
	global applex
	global appley
	global snake_length
	global almighty

	global x
	global y

	x, y = get_pos_x(), get_pos_y()
	snake_length = 1

	change_hat(Hats.Dinosaur_Hat)
	applex, appley = measure()
	# go to center line
	if y > top_line_y:
		measure_and_move(South, y - top_line_y)
	elif y < bottom_line_y:
		measure_and_move(North, bottom_line_y - y)

	detours_taken_this_lap = 0
	ignore_detours = False
	almighty = False
	# follow center line
	while True:
		dir = None
		x, y = get_pos_x(), get_pos_y()

		if y == top_line_y:
			if x == 0:
				detours_taken_this_lap = 0
			if not ignore_detours and ( almighty or (x % 2 == 0 and detours_taken_this_lap < detours_needed_per_lap)):
				if not do_detour(North, detour_length):
					break
				ignore_detours = True
				detours_taken_this_lap += 1
				continue
			if not ignore_detours and appley > top_line_y and x // 2 == applex // 2 and x % 2 == 0:
				if not do_detour(North, appley - top_line_y):
					break
				ignore_detours = True
				continue
			if x == end:
				dir = South
			else:
				dir = East
		elif y == bottom_line_y:
			if not ignore_detours and ( almighty or (x % 2 == 1 and detours_taken_this_lap < detours_needed_per_lap)):
				if not do_detour(South, detour_length):
					break
				ignore_detours = True
				detours_taken_this_lap += 1
				continue
			if not ignore_detours and appley < bottom_line_y and x // 2 == applex // 2 and x % 2 == 1:
				if not do_detour(South, bottom_line_y - appley):
					break
				ignore_detours = True
				continue
			if x == 0:
				dir = North
			else:
				dir = West
		ignore_detours = False
		if not measure_and_move(dir, 1):
			break
	change_hat(Hats.Dinosaur_Hat)

def satisfy_cost(bone_cost):
	global ws
	global end
	global top_line_y
	global bottom_line_y
	global detour_length
	global length_for_almighty

	ws = get_world_size()
	length_for_almighty = (ws*ws)/2
	end = ws - 1
	top_line_y = ws // 2
	bottom_line_y = top_line_y - 1 
	detour_length = bottom_line_y
	
	while num_items(Items.Bone) < bone_cost:
		do_full_board()
	change_hat(Hats.Straw_Hat)

if __name__ == "__main__":
	set_world_size(14)
	satisfy_cost(num_items(Items.Bone) + 1000000)
#	satisfy_cost(num_items(Items.Bone) + 33488928)
