import mazereuse
import goals

set_world_size(32)
#mazereuse.do_until(goals.create_goal(None, { Items.Gold: 9863168}))
mazereuse.do_until(goals.create_goal(None, { Items.Gold: num_items(Items.Gold)+ 2000000}))

