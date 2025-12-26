def handle():
	if get_ground_type() != Grounds.Grassland:
		harvest()
		till()
		plant(Entities.Bush)
	elif get_entity_type() != Entities.Bush:
		plant(Entities.Bush)
	elif can_harvest():
		harvest()
		plant(Entities.Bush)