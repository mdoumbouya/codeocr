# 1 karel Problem - Karel home
from Karel. Stanfordkarel import *
# This program defines a main function which should make karel
# move to the beeper, pick it up and return home
def main () :
    get_Out ()
    pick_food ()
    get back_ home ()
# pre : Karel facing east, at the corner of starting position
# post: karel facing east, outside the home, at the position of beeper
def get_out () :
    turn_right ( )
    move ()
    turn_left ()
    move ()
    move ()
    move ()
# post: Karel facing west, at the position of beeper
def pick-food ():
    pick_beeper ()
    turn- around ()
# post: Karel facing east, at the corner of starting position
def get_ back_home () :
    move ()
    Move ()
    move ()
    turn right ()
    move ()
    turn right ()
def turn right () ;
    for i in range (3) :
    turn-left ()
def
    turn-around () :
    turn_left ()
    turn_kft ()
if_ name_ == '-main -:
main ()
