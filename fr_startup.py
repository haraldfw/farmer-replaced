def do():
	harvest()
	move(North)
	harvest()
	move(North)
	harvest()
	move(North)

def harvest_until(goal_func):
	while not goal_func():
		harvest()

def wait_and_harvest_until(goal_func):
	while not goal_func():
		if can_harvest():
			harvest()

def move_and_harvest_until(goal_func):
	while not goal_func():
		harvest()
		move(North)
		harvest()
		move(North)
		harvest()
		move(North)
