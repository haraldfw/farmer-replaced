def create_goal(goal_unlock, item_requirements=None):
	# if goal_unclock is not None, then populate item_requirements with costs from that unlock
	if goal_unlock != None:
		if item_requirements == None:
			item_requirements = get_cost(goal_unlock)
		else:
			costs = get_cost(goal_unlock)
			for item in costs:
				cost = costs[item]
				if item in item_requirements:
					item_requirements[item] += cost
				else:
					item_requirements[item] = cost

	if len(item_requirements) == 1:
		for item in item_requirements:
			def single_goal():
				return num_items(item) >= item_requirements[item]
			return single_goal

	def multi_goal():
		for item in item_requirements:
			if num_items(item) < item_requirements[item]:
				return False
		return True
	return multi_goal

def infinite_goal():
	return False
