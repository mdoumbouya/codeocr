# 1 karel Problem - karel home
from karel.stanfordkarel import *
# This program defines a main function which should make karel 
# move to beeper, pick it up and return home.

def main():
    get_out()
    pick_food()
    get_back_home()
# pre: karel facing east, at the corner of starting position
# post: karel facing east, outside the home, at the position of beeper

def get_out():
    turn_right()
    move()
    turn_left()
    move()
    move()
    move()
    move()
# post: karel facing west, at the position of beeper

def pick_food():
    pick_beeper()

def get_back_home():
    move()
    move()
    move()
    turn_right()
    move()
    turn_right()

def turn_right():
    for i in range(3):
        turn_left()

def turn_around():
    turn_left()
    turn_left()
if __name__ == '__main__':
    main()
