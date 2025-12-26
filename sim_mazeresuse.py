sim_unlocks = Unlocks
sim_items = {Items.Carrot : 99999999, Items.Hay : 99999999, Items.Weird_Substance: 99999999}
sim_globals = {}
seed = 0
speedup = 64

run_time = simulate("mazereuse", sim_unlocks, sim_items, sim_globals, seed, speedup)
print(run_time)
