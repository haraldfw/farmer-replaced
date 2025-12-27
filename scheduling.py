import util
import goals
import fr_power
import fr_startup
import fr_bush
import fr_bush_multi
import fr_tree
import fr_pumpkin
import fr_power
import fr_polyculture
import fr_cactus
import fr_snake
import mazereuse

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

def apply_item_if_needed(dict, item, value):
	if num_items[item] >= value:
		# not needed, do not apply
		return False

	if item in dict:
		dict[item] += value
	else:
		dict[item] = value
	return True

def calc_pre_task_costs(costs):
	if Items.Bone in costs:
		cost_scale = costs[Items.Bone]
		if not apply_item_if_needed(costs, Items.Cactus, cost_scale*2):
			return
	if Items.Cactus in costs:
		cost_scale = costs[Items.Cactus]
		if not apply_item_if_needed(costs, Items.Pumpkin, cost_scale*2):
			return
	if Items.Pumpkin in costs:
		cost_scale = costs[Items.Pumpkin]
		if not apply_item_if_needed(costs, Items.Carrot, cost_scale):
			return
	if Items.Carrot in costs:
		cost_scale = costs[Items.Carrot]
		if not apply_item_if_needed(costs, Items.Hay, cost_scale):
			return
		if not apply_item_if_needed(costs, Items.Wood, cost_scale):
			return

def satisfy_costs(costs, ignore_zero_power=False):
	ensure_power()

	# TODO: create a list of goal_funcs and do_until-func tuples instead of accumulating costs in a large dict
	calc_pre_task_costs(costs)

	if Items.Hay in costs or Items.Wood in costs or Items.Carrot in costs:
		# harvest
		# util.wait_and_harvest
		# fr_move_and_harvest.do
		# fr_bush.do_single_lane
		# fr_bush_multi.do_until
		# fr_tree.do_until
		if num_unlocks(Unlocks.Speed) == 0:
			# we are in the beginning stage, no unlocks
			pass
			
	if Items.Pumpkin in costs:
		fr_pumpkin.do_until(costs)
	if Items.Cactus in costs:
		fr_cactus.do_until(costs)
	if Items.Bone in costs:
		fr_snake.do_until(costs)

def do_full_reset():
	unlock_order = [
		Unlocks.Speed,
		Unlocks.Expand,
		Unlocks.Plant,
		Unlocks.Speed,
		Unlocks.Expand,
		Unlocks.Carrots,
		Unlocks.Speed,
		Unlocks.Trees,
		Unlocks.Watering,
		Unlocks.Grass,
		Unlocks.Expand,
		Unlocks.Watering,
		Unlocks.Expand,
		Unlocks.Trees,
		Unlocks.Carrots,
		Unlocks.Carrots,
		Unlocks.Speed,
		Unlocks.Speed,
		Unlocks.Watering,
		Unlocks.Grass,
		Unlocks.Grass,
		Unlocks.Trees,
		Unlocks.Sunflowers,
		Unlocks.Pumpkins,
		Unlocks.Expand,
		Unlocks.Polyculture,
		Unlocks.Fertilizer,
		Unlocks.Trees,
		Unlocks.Fertilizer,
		Unlocks.Fertilizer,
		Unlocks.Fertilizer,
		Unlocks.Pumpkins,
		Unlocks.Pumpkins,
		Unlocks.Cactus,
		Unlocks.Dinosaurs,
		Unlocks.Hats,
		Unlocks.Polyculture,
		Unlocks.Expand,
		Unlocks.Carrots,
		Unlocks.Carrots,
		Unlocks.Trees,
		Unlocks.Grass,
		Unlocks.Watering,
		Unlocks.Watering,
		Unlocks.Watering,
		Unlocks.Pumpkins,
		Unlocks.Cactus,
		Unlocks.Mazes,
		Unlocks.Mazes,
		Unlocks.Mazes,
		Unlocks.Expand,
		Unlocks.Grass,
		Unlocks.Megafarm,
		Unlocks.Megafarm,
		Unlocks.Trees,
		Unlocks.Dinosaurs,
		Unlocks.Dinosaurs,
	]
	for to_unlock in unlock_order:
		satisfy_costs(get_cost(to_unlock))
		unlock(to_unlock)
