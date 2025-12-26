import util
import goals

if __name__ == "__main__":
	clear()
	set_world_size(5)
	do_until(util.create_goal(None, {Items.Bone: 33488928}))