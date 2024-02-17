from karel.stanfordkarel import *
"""
karel should fill the world with beepers.
"""

def main():
    #decompostion using a function name for
    #each associated activity
    while left_is_clear():
        fill_one_row()
        return_to_row_start()
        move_up()
    #rewritw code after while loop to overcomw
    #fencepost bug
    fill_one_row()
