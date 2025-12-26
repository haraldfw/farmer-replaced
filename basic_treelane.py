import util

def create_task(start_lane_x, use_carrot_as_spacer=False):
	def f():
		change_hat(Hats.Tree_Hat)
		util.move_to(start_lane_x, 0)
		while True:
			if (get_pos_y() + start_lane_x) % 2 == 0:
				pass # tree tile, already setup with grass
			elif use_carrot_as_spacer:
				# only carrot needs setup
				util.ensure_ground(Grounds.Soil)
				util.ensure_plant(Entities.Carrot)
			move(North)
			if get_pos_y() == 0:
				break
		while True:
			if (get_pos_y() + start_lane_x) % 2 == 0:
				harvest()
				plant(Entities.Tree)
				util.water_to(0.6)
			else:
				harvest()
				if use_carrot_as_spacer:
					plant(Entities.Carrot)
					util.water_to(0.25)
			move(North)
	return f
		
