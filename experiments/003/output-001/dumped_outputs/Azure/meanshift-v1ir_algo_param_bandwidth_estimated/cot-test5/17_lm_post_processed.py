from karel.stanfordkarel import *

def main():
    turn_left()
    tower_N()
    tower_SC()
    move_4x()
    turn_left()
    tower_N()
    tower_SC()

def tower_SC():
    turn_3x()
    tower()
    turn_left()

def tower_N():
    tower()
    turn_3x()
    move_4x()

def tower():
    for i in range(5):
        if front_is_clear():
            put_beeper()
            move()
        else:
            put_beeper()

def turn_3x():
    turn_left()
    turn_left()
    turn_left()

def move_4x():
    move()
    move()
    move()
    move()
if __name__ == '__main__':
    main()
