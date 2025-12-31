sim_unlocks = {}
for u in Unlocks:
	sim_unlocks[u] = num_unlocked(u)
sim_unlocks[Unlocks.Megafarm] = 4
sim_items = {
	Items.Carrot: 123123123,
	Items.Water: 200000,
	Items.Power: 2000000,
	Items.Fertilizer: 20000000,
	Items.Weird_Substance: 2000000,
}
sim_globals = {"a" : 13}
seed = -1
speedup = 10

run_time = simulate("fr_pumpkin", sim_unlocks, sim_items, sim_globals, seed, speedup)
quick_print(run_time)

#leaderboard_run(Leaderboards.Dinosaur, "fr_snake", 200)
