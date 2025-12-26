import util
import fr_power
import goals

def ensure_power():
	if (num_unlocks(Unlocks.Sunflowers)) < 1:
		return
	if num_items(Items.Power) < 100:
		ticks_at_start = get_tick_count()
		quick_print("power almost depleted, creating more...")
		goal_func = goals.create_goal(None, { Items.Power: 5000 })
		do_until(goal_func)
		if goal_unlock != None:
			unlock(goal_unlock)
		quick_print("unlocked", goal_unlock, "in", (get_tick_count() - ticks_at_start)/400,"seconds")

def run_do_until(do_until, goal_unlock, item_requirements=None):
	ticks_at_start = get_tick_count()
	quick_print("starting", do_until, "until", goal_unlock)
	goal_func = goals.create_goal(goal_unlock, item_requirements)
	do_until(goal_func)
	if goal_unlock != None:
		unlock(goal_unlock)
	quick_print("unlocked", goal_unlock, "in", (get_tick_count() - ticks_at_start)/400,"seconds")

def do_single_until_unlock(single_action, goal_unlock):
	ticks_at_start = get_tick_count()
	quick_print("starting", single_action, "until", goal_unlock)
	goal = goals.create_goal(goal_unlock)
	while not goal():
		single_action()
	unlock(goal_unlock)
	quick_print("unlocked", goal_unlock, "in", (get_tick_count() - ticks_at_start)/400,"seconds")
