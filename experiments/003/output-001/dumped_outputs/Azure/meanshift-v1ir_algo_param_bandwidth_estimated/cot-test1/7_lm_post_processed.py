from karel.stanfordkarel import *
# Karel should fill the world with beepers.
1100

def main () :
# decomposition using a function name for
# each associated activity
while left_is_clear ():
    fill_one_row()
    return_to_row_start ()
    move_up()
# rewrite code after while loop to overcome
# fencepost bug
fill_one_row()
