import util

def x_pos_to_index(startx, starty):
	return get_pos_x() - startx

def y_pos_to_index(startx, starty):
	return get_pos_y() - starty

def move_to_index_x(index, startx, starty):
	return util.move_to_x(startx + index)

def move_to_index_y(index, startx, starty):
	return util.move_to_y(starty + index)

def create_task(startx, starty=0, forward_dir = North):
	def f():
		backward_dir = South
		endpos = starty + 10
		get_pos = get_pos_y
		pos_to_index = y_pos_to_index
		move_to_index = move_to_index_y

		if forward_dir == East:
			endpos = startx + 10
			get_pos = get_pos_x
			backward_dir = West
			pos_to_index = x_pos_to_index
			move_to_index = move_to_index_x

		change_hat(Hats.Sunflower_Hat)
		util.move_to(startx, starty)
		# 10 indices, one for each flower
		flowers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		for i in range(10):
			till()
			plant(Entities.Sunflower)
			index = pos_to_index(startx, starty)
			flowers[i] = measure()
			if index < 10:
				move(forward_dir)

		while(True):
			biggest_value = 0
			biggest_index = -1
			for i in range(10):
				val = flowers[i]
				if val > biggest_value:
					biggest_value = val
					biggest_index = i

			move_to_index(biggest_index, startx, starty)
			fert_used = 0
			while not can_harvest():
				# wait until flower is grown
				if num_items(Items.Power) < 300 and fert_used < 1:
					use_item(Items.Fertilizer)
					fert_used += 1
				continue
			if fert_used > 0:
				use_item(Items.Weird_Substance)
			harvest()
			plant(Entities.Sunflower)
			util.water_to_max()
			flowers[biggest_index] = measure()
	return f
