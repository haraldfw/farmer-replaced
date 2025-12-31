def do():
	harvest()
	move(North)
	harvest()
	move(North)
	harvest()
	move(North)

def basic_harvest_satisfy_hay_cost(hay_cost):
	while num_items(Items.Hay) < hay_cost:
		harvest()

def wait_and_harvest_satisfy_cost(hay_cost):
	while num_items(Items.Hay) < hay_cost:
		if can_harvest():
			harvest()

def move_and_harvest_satisfy_cost(goal_func):
	while num_items(Items.Hay) < hay_cost:
		harvest()
		move(North)
		harvest()
		move(North)
		harvest()
		move(North)
