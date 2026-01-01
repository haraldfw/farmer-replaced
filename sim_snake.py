sim_unlocks = {}
for u in Unlocks:
	sim_unlocks[u] = num_unlocked(u)
#sim_unlocks[Unlocks.Megafarm] = 2
sim_items = {
	Items.Carrot: 123123123,
	Items.Cactus: 200000000,
	Items.Water: 200000,
	Items.Power: 2000000,
	Items.Fertilizer: 20000000,
	Items.Weird_Substance: 200000000,
}
sim_globals = {"sim_goal" : 2000000, "sim_ws": 32}
seed = -1
speedup = 1000

#run_time = simulate("fr_substance_abuse", sim_unlocks, sim_items, sim_globals, seed, speedup)
run_time = simulate("fr_snake", sim_unlocks, sim_items, sim_globals, seed, speedup)

quick_print(run_time)

#leaderboard_run(Leaderboards.Dinosaur, "fr_snake", 200)
