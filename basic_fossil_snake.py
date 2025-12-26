import util
# States
stateFollowCircle = 0
stateSpikeLeft = 1
stateSpikeLeftReturn = 2
stateSpikeRight = 3
stateSpikeRightReturn = 4

def create_task():
	def f():
		state = stateFollowCircle
		world_size = get_world_size()

		change_hat(Hats.Dinosaur_Hat)
		
		endx = world_size - 1
		endy = world_size - 1
		applex, appley = measure()
		# circle routine
		while True:
			x = get_pos_x()
			y = get_pos_y()
			
			if state == stateFollowCircle:
				if x == applex and y == appley:
					# this can happen if the apple is on the circle path
					applex, appley = measure()
				elif applex != 0 and applex != endx and y != 0 and y != endy and y == appley:
					if x == 0 and appley < endy - 1:
						state = stateSpikeRight
						move(East)
					elif x == endx and appley > 1:
						state = stateSpikeLeft
						move(West)
					elif x == 0:
						move(North)
					else:
						move(South)
				elif x == 0:
					if y == endy:
						move(East)
					else:
						move(North)
				elif y == 0:
					if x == 0:
						move(North)
					else:
						move(West)
				elif x == endx:
					if y == 0:
						move(West)
					else:
						move(South)
				elif y == endy:
					if x == endx:
						move(South)
					else:
						move(East)
			elif state == stateSpikeRight:
				if x < applex:
					move(East)
				else:
					# we are inside the apple
					applex, appley = measure()
					state+=1
					move(North)
			elif state == stateSpikeRightReturn:
				if x > 0:
					move(West)
				else:
					state = stateFollowCircle
					move(North)
			elif state == stateSpikeLeft:
				if x > applex:
					move(West)
				else:
					applex, appley = measure()
					state+=1
					move(South)
			elif state == stateSpikeLeftReturn:
				if x < endy:
					move(East)
				else:
					state = stateFollowCircle
					move(South)
			
			
			
		# zig zag max length routine
		while True:
			for x in range(world_size):
				if not util.move_to_x(x):
					change_hat(Hats.Traffic_Cone)
					change_hat(Hats.Dinosaur_Hat)
					continue
				range_start = 1
				range_end = world_size
				step = 1
				if x % 2 != 0:
					range_start = world_size-1
					range_end = 0
					step = -1
				for y in range(range_start, range_end, step):
					if not util.move_to_y(y):
						change_hat(Hats.Traffic_Cone)
						change_hat(Hats.Dinosaur_Hat)
						continue
			if not move(South):
				change_hat(Hats.Traffic_Cone)
				change_hat(Hats.Dinosaur_Hat)
				continue
			for x in range(world_size-1):
				if not move(West):
					change_hat(Hats.Traffic_Cone)
					change_hat(Hats.Dinosaur_Hat)
					continue
			if not move(North):
				change_hat(Hats.Traffic_Cone)
				change_hat(Hats.Dinosaur_Hat)
				continue
			
	return f

if __name__ == "__main__":
	clear()
	set_world_size(14)
	create_task()()