from karel.stanfordkarel import *

def main():
    while front_is_clear():
        fill_tower()

def fill_tower():
    while front_is_clear():
        put_beeper()
        move()
    put_beeper()
    column_return()

def column_return():
    while front_is_blocked():
        turn_around()
    while front_is_clear():
        move()
    next_tower()

def turn_around():
    for i in range(2):
        turn_left()

def next_tower():
    if right_is_clear():
        move()
        turn_right()
    else:
        turn_around()
        while front_is_clear():
            move()

def turn_right():
    for i in range(3):
        turn_left()
if __name__ == '__main__':
    main()
