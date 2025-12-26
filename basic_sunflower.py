import util

def create_task(lane_x):
	def f():
		change_hat(Hats.Sunflower_Hat)
		util.move_to(lane_x, 0)
		while(True):
			till()
			plant(Entities.Sunflower)
			move(North)
			if get_pos_y() == 0:
				break
		biggest_value = 0
		y_biggest = -1
		while(True):
			val = measure()
			if val > biggest_value:
				biggest_value = val
				y_biggest = get_pos_y()
			move(North)
			if get_pos_y() == 0:
				util.move_to_y(y_biggest)
				while not can_harvest():
					# wait until flower is grown
					continue
				harvest()
				plant(Entities.Sunflower)
				util.water_to_max()
				biggest_value = 0
				util.move_to_y(0)
	return f