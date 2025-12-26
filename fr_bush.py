import util

def do_single_lane():
	if util.harvest_if_possible():
		plant(Entities.Bush)
	move(North)
	if util.harvest_if_possible():
		plant(Entities.Bush)
	move(North)
	if util.harvest_if_possible():
		plant(Entities.Bush)
	move(North)

def do_multi_lane():
	do_single_lane()
	move(East)
	do_single_lane()
	move(East)
	do_single_lane()
	move(East)
