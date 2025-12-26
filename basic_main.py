import basic_grass
import basic_tree
import basic_carrot
import basic_pumpkin
import basic_cactus
import basic_sunflowerpatch
import basic_treelane
import basic_pumpkinpatch
import basic_cactuspatch

clear()
world_size = get_world_size()

change_hat(Hats.Carrot_Hat)

def find_wanted_crop():
	x = get_pos_x()
	if x < 12:
		return None
	elif  x < 12:
		return basic_grass
	elif x < 26:
		return basic_pumpkin
	else:
		return basic_cactus

def run():
	#spawn_drone(sunflower.create_task(26))
	spawn_drone(basic_treelane.create_task(0))
	spawn_drone(basic_treelane.create_task(1, True))
	spawn_drone(basic_cactuspatch.create_task(2,12, 6, 6))
	spawn_drone(basic_sunflowerpatch.create_task(2,6, 6, 6))
	spawn_drone(basic_pumpkinpatch.create_task(2,0, 6, 6))
	wanted_crop = find_wanted_crop()
	while(True):
		if wanted_crop != None:
			if num_drones() < max_drones():
				spawn_drone(wanted_crop.create_row_task(world_size))
			else:
				wanted_crop.create_row_task(world_size)()
				move(North)
		move(East)
		wanted_crop = find_wanted_crop()

if __name__ == "__main__":
	run()
