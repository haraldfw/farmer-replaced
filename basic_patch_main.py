import basic_treelane
import basic_pumpkinpatch
import basic_sunflowerpatch
import basic_cactuspatch
import basic_fossil_snake

world_size = get_world_size()
change_hat(Hats.Carrot_Hat)

def do_complete_farm():
	clear()
	set_world_size(32)
	change_hat(Hats.The_Farmers_Remains)
	spawn_drone(basic_treelane.create_task(0))
	spawn_drone(basic_treelane.create_task(1, True))
	
	spawn_drone(basic_pumpkinpatch.create_task(2,18, 6, 6))
	spawn_drone(basic_sunflowerpatch.create_task(2,6, 6, 6))
	spawn_drone(basic_cactuspatch.create_task(2,0, 6, 6))
	spawn_drone(basic_cactuspatch.create_task(2,12, 6, 6))
	spawn_drone(basic_cactuspatch.create_task(2,25, 11, 7))

	spawn_drone(basic_pumpkinpatch.create_task(8,0, 6, 6))
	spawn_drone(basic_cactuspatch.create_task(8,6, 6, 6))
	spawn_drone(basic_pumpkinpatch.create_task(8,12, 6, 6))
	spawn_drone(basic_cactuspatch.create_task(8,18, 6, 6))
	
	spawn_drone(basic_cactuspatch.create_task(14,0, 6, 6))
	spawn_drone(basic_pumpkinpatch.create_task(14,6, 6, 6))
	spawn_drone(basic_cactuspatch.create_task(14,12, 6, 6))
	spawn_drone(basic_pumpkinpatch.create_task(14,18, 6, 6))
	spawn_drone(basic_cactuspatch.create_task(14,24, 6, 6))
	
	spawn_drone(basic_pumpkinpatch.create_task(20,0, 6, 6))
	spawn_drone(basic_cactuspatch.create_task(20,6, 6, 6))
	spawn_drone(basic_pumpkinpatch.create_task(20,12, 6, 6))
	spawn_drone(basic_cactuspatch.create_task(20,18, 6, 6))
	spawn_drone(basic_pumpkinpatch.create_task(20,24, 6, 6))
	
	spawn_drone(basic_cactuspatch.create_task(26,0, 6, 6))
	spawn_drone(basic_pumpkinpatch.create_task(26,6, 6, 6))
	spawn_drone(basic_cactuspatch.create_task(26,12, 6, 6))
	spawn_drone(basic_pumpkinpatch.create_task(26,18, 6, 6))
	spawn_drone(basic_cactuspatch.create_task(26,24, 6, 6))

def run_snake():
	set_world_size(32)
	spawn_drone(basic_fossil_snake.create_task())

if __name__ == "__main__":
	clear()
	do_complete_farm()
