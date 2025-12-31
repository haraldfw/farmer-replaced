import util
import goals
import fr_power
import fr_startup
import fr_bush
import fr_bush_multi
import fr_tree
import fr_substance
import fr_pumpkin
import fr_power
import fr_polyculture
import fr_cactus
import fr_snake
import mazereuse

def ensure_power():
	if (num_unlocked(Unlocks.Sunflowers)) < 1:
		return
	if num_items(Items.Power) < 100:
		ticks_at_start = get_tick_count()
		quick_print("power almost depleted, creating more...")
		fr_power.satisfy_cost(5000)
		quick_print("power replenished")

def apply_item_if_needed(dict, item, value):
	if num_items(item) >= value:
		# not needed, do not apply
		return False

	if item in dict:
		dict[item] += value
	else:
		dict[item] = value
	return True

# this function populates the given cost-dict with the ingredients of the dict's content's costs.
# For example if the dict contains a cost of 200 carrots, then the array will be populated with
# 200 wood and 200 hay, because that is what it costs to plant 200 carrots.
# As a performance measure, we skip adding any items of which the cost is already satisfied,
# using the num_items built-in
def calc_pre_task_costs(costs):
	if Items.Weird_Substance in costs:
		substance_cost = costs[Items.Weird_Substance]
		ws = get_world_size()
		# we need to place an apple on every tile of the board for a full board to be completed
		ws_squared = ws*ws
		full_board_cost = ws_squared*get_cost(Entities.Cactus)[Items.Pumpkin]
		boards_needed = util.ceil(substance_cost/(ws_squared*6/2))
		# TODO FIXME a cactus field where catus gives 41.3k cactus only gives 144 weird substance, figure out why
		# Likely because field is 12x12 = 144 large, so we only get one weird ubstance per plant harvested, this means we should go for pumpkin-harvests instead of cacti, because they are cheaper AND they are faster.abs
		# TODO: switch substance-farm to pumpkins
		if not apply_item_if_needed(costs, Items.Pumpkin, full_board_cost * boards_needed):
			return
	if Items.Bone in costs:
		bone_cost = costs[Items.Bone]
		ws = get_world_size()
		# we need to place an apple on every tile of the board for a full board to be completed
		ws_squared = ws*ws
		full_board_cost = ws_squared*get_cost(Entities.Apple)[Items.Cactus]
		boards_needed = util.ceil(bone_cost/((ws_squared-1)**2))

		if not apply_item_if_needed(costs, Items.Cactus, full_board_cost * boards_needed):
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

def get_if_exists(dict, key):
	if key in dict:
		return dict[key]
	return 0 

def satisfy_costs(costs, ignore_zero_power=False):
	ensure_power()

	calc_pre_task_costs(costs)

	hay_cost = get_if_exists(costs, Items.Hay)
	wood_cost = get_if_exists(costs, Items.Wood)
	carrot_cost = get_if_exists(costs, Items.Carrot)
	pumpkin_cost = get_if_exists(costs, Items.Pumpkin)
	cactus_cost = get_if_exists(costs, Items.Cactus)
	bone_cost = get_if_exists(costs, Items.Bone)
	gold_cost = get_if_exists(costs, Items.Gold)
	substance_cost = get_if_exists(costs, Items.Weird_Substance)

		# harvest
		# util.wait_and_harvest
		# fr_move_and_harvest.do
		# fr_bush.do_single_lane
		# fr_bush_multi.do_until
		# fr_tree.do_until
	reqs = {}
	if hay_cost:
		reqs[Items.Hay] = hay_cost
		hay_cost += 200
	if wood_cost:
		reqs[Items.Wood] = wood_cost
		wood_cost += 200
	if carrot_cost:
		reqs[Items.Carrot] = carrot_cost
	if reqs:
		# at least one of the trifecta is required, figure out what do_until(s) to execute and execute them
		if num_unlocked(Unlocks.Polyculture) > 0:
			fr_polyculture.satisfy_costs(hay_cost, wood_cost, carrot_cost)
		else:
			if num_unlocked(Unlocks.Carrots):
				if num_unlocked(Unlocks.Trees):
					fr_tree.satisfy_costs(hay_cost, wood_cost, carrot_cost)
				else:
					fr_bush_multi.satisfy_costs(hay_cost, wood_cost, carrot_cost)
			else:
				if hay_cost:
					if num_unlocked(Unlocks.Speed) == 0:
						# we are in the initial stage, no unlocks, do harvest spam
						fr_startup.basic_harvest_satisfy_hay_cost(hay_cost)
					elif num_unlocked(Unlocks.Speed) == 1:
						fr_startup.wait_and_harvest_satisfy_cost(hay_cost)
					elif num_unlocked(Unlocks.Expand) == 1:
						fr_startup.move_and_harvest_satisfy_cost(hay_cost)
				if wood_cost:
					quick_print(get_world_size(), num_unlocked(Unlocks.Expand))
					fr_bush.satisfy_cost(wood_cost)

	if substance_cost:
		fr_substance.satisfy_cost(substance_cost)

	if gold_cost:
		mazereuse.satisfy_cost(gold_cost)

	if pumpkin_cost:
		fr_pumpkin.satisfy_cost(pumpkin_cost)
	if cactus_cost:
		fr_cactus.satisfy_cost(cactus_cost)
	if bone_cost:
		fr_snake.satisfy_cost(bone_cost)

def do_full_reset():
	unlock_order = [
		Unlocks.Speed,
		Unlocks.Expand,
		Unlocks.Plant,
		Unlocks.Speed,
		Unlocks.Expand,
		Unlocks.Carrots,
		Unlocks.Grass,
		Unlocks.Speed,
		Unlocks.Trees,
		Unlocks.Watering,
		Unlocks.Expand,
		Unlocks.Watering,
		Unlocks.Expand,
		Unlocks.Trees,
		Unlocks.Grass,
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
#		Unlocks.Hats,
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
		ticks_at_start = get_tick_count()
		satisfy_costs(get_cost(to_unlock))
		if not unlock(to_unlock):
			assert()
		quick_print("unlocked", to_unlock, "in", (get_tick_count() - ticks_at_start)/400,"seconds")
