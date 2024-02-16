from karel.stanfordkarel import *

def main():
turn_left()
while front_is_clear():
    turn_right()
    fill_row()
    return_to_home()
    jump_row()
turn_right()
fill_row()
return_to_home()
while front_is_clear():
    move()

def fill_row():
while front_is_clear():
    put_beeper()
    move()
put_beeper()
