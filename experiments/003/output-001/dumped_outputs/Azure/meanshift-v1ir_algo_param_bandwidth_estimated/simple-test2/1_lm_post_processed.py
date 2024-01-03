from karel.stanfordkarel import *
# This program makes Karel pick up
# a beeper and go back into her house.

def main():
    # Move to the beeper.
    move_beeper()
    # Pick the beeper up.
    pick_beeper()
    # Return to Karel's starting point.
    go_back()
# This function moves Karel to the beeper.

def move_beeper():
    for i in range(2):
        move()
        turn_right()
        move()
        turn_left()
        move()
# this function return to Karel's starting point

def go_back():
    for i in range(2):
        turn_left()
    for i in range(3):
        move()
        turn_right()
        move()
        turn_right()

def turn_right():
    for i in range(3):
        turn_left()
if __name__ == '__main__':
    main()
