
watering_threshold = 0.2
def create_row_task(world_size=get_world_size()):
	def task():
		while True:
			handle()
			if get_pos_y()+1 == world_size:
				break
			move(North)
	return task

def handle():
	if get_water() < watering_threshold:
		use_item(Items.Water)

	if get_ground_type() != Grounds.Grassland:
		harvest()
		till()
		plant(Entities.Tree)
	elif can_harvest():
		harvest()
		plant(Entities.Tree)
		#if get_pos_x() == 2:
			#use_item(Items.Fertilizer)
	elif get_entity_type() != Entities.Tree:
		plant(Entities.Tree)