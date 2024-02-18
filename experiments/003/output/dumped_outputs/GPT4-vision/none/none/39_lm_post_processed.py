from karel.stanfordkarel import *

def main():
    move_to_beep()
    pick_beeped()
    turn_around()
    return_to_stert()

def move_to_beeper():
    while front_is_clear():
        move()
    turn_right()
    move()
    turn_left()
    move()

def turn_around():
    turn_left()
    turn_left()
