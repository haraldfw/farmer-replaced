import util
# TODO: only check pumpkins where known dead pumpkins where, use move_to and append coords for dead pumpkins to a list to check, iterate over list until empty

def plant_and_water_pumpkin():
	plant(Entities.Pumpkin)

def create_task(startx, starty, width, height):
	endx = startx+width
	endy = starty+height
	def f():
		change_hat(Hats.Pumpkin_Hat)
		util.move_to(startx, starty)
		util.traverse_zig_zag(startx, starty, width, height, till)

		while True:
			util.traverse_zig_zag(startx, starty, width, height, plant_and_water_pumpkin)
			deads = []
			def update():
				global deads
				while not can_harvest():
					if get_entity_type() == Entities.Dead_Pumpkin:
						harvest()
						plant(Entities.Pumpkin)
						util.water_to(0.5)
						deads.append((get_pos_x(), get_pos_y()))
						return
			util.traverse_zig_zag(startx, starty, width, height, update)
			while deads:
				i = 0
				for _ in range(len(deads)):
					deadx, deady = deads[i]
					util.move_to(deadx, deady)
					while get_entity_type() == Entities.Pumpkin and not can_harvest():
						continue
					if get_entity_type() == Entities.Dead_Pumpkin:
						harvest()
						plant(Entities.Pumpkin)
						util.water_to(0.5)
						i += 1
					else:
						deads.pop(i)
			use_item(Items.Fertilizer)
			harvest()				

	return f

if __name__ == "__main__":
	clear()
	set_world_size(16)
	create_task(0, 0, 15, 15)()
