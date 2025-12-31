import util

def satisfy_cost(substance_cost):
	clear()

	util.move_to(4,4)

	while num_items(Items.Weird_Substance) < substance_cost:
		util.water_to(0.75)
		plant(Entities.Tree)
		if Entities.Grass in get_companion():
			use_item(Items.Fertilizer)
		harvest()
