import util
import goals

def create_spam_substance_task(goal_func, substance_amount):
	def f():
		while not goal_func():
			while use_item(Items.Weird_Substance, substance_amount):
				continue
			if get_entity_type() == Entities.Treasure:
				if not use_item(Items.Weird_Substance, substance_amount):
					harvest()
					plant(Entities.Bush)
					use_item(Items.Weird_Substance,substance_amount)				
	return f

def do_until(goal_func):
	ws = 3
	mx_dr = max_drones()
	# find the biggest ws we can have
	while True:
		new_ws = ws + 1
		if new_ws**2 > mx_dr:
			break
		ws = new_ws
	
	substance_amount = ws * 2**(num_unlocked(Unlocks.Mazes)-1)
	set_world_size(ws)
	wsr = range(ws-1, -1, -1)
	for x in wsr:
		for y in wsr:
			util.move_to(x, y)
			if x==0 and y ==0:
				plant(Entities.Bush)
				use_item(Items.Weird_Substance,substance_amount)					
				create_spam_substance_task(goal_func, substance_amount)()
			else:
				spawn_drone(create_spam_substance_task(goal_func, substance_amount))


if __name__ == "__main__":
	clear()
	set_world_size(5)
	#do_until(goals.infinite_goal)
	#do_until(goals.create_goal(None, {Items.Gold: 616448}))
	goal = goal
	goal_func = goals.infinite_goal
	if goal:
		goal_func = goals.create_goal(None, {Items.Gold: goal})
	do_until(goal_func)
