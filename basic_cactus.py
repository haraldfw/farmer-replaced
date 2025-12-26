def create_row_task(world_size=get_world_size()):
	def task():
		while True:
			handle()
			if get_pos_y()+1 == world_size:
				break
			move(North)
	return task

def handle():
	if get_ground_type() != Grounds.Soil:
		harvest()
		till()
		plant(Entities.Cactus)
	elif can_harvest():
		harvest()
		plant(Entities.Cactus)
	elif get_entity_type() != Entities.Cactus:
		plant(Entities.Cactus)