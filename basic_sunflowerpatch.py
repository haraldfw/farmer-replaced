import util
# TODO: break when there are <10 sunflowers left. Keep track of how many are harvested
def create_petal_list():
	petals = []
	for i in range(7, 16):
		petals.append([])
	return petals

def create_task(startx, starty, width, height):
	def f():
		change_hat(Hats.Sunflower_Hat)
		petals = create_petal_list()
		util.move_to(startx, starty)
		util.traverse_zig_zag(startx, starty, width, height, till)

		def ensure_and_measure_watered_sunflower():
			global petals
			if get_entity_type() != Entities.Sunflower:
				plant(Entities.Sunflower)
			util.water_to(0.5)
			petals[15-measure()].append([get_pos_x(), get_pos_y()])
		while True:
			util.traverse_zig_zag(startx, starty, width, height, ensure_and_measure_watered_sunflower)
			i = 0
			flowersLeft = height*width
			for petalCoords in petals:
				if flowersLeft <= 8:
					petals[i]=[]
					i+=1
					continue
				for coord in petalCoords:
					util.move_to(coord[0], coord[1])
					while not can_harvest():
						pass
					harvest()
					flowersLeft -= 1
					if flowersLeft <= 8:
						break
				petals[i]=[]
				i+=1
	return f

if __name__ == "__main__":
	clear()
	set_world_size(16)
	create_task(2, 2, 12, 12)()
