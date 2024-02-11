from karel.stanfordkarel import *

def main():
    turn_left()
    turn_N()
    turn_SC()
    move_xr()
    turn_left()
    turn_N()
    turn_SC()

def turn_SC():
    turn_3x()
    tower()
    turn_left()

def turn_N():
    tower()
    turn_3x()
    move_xr()

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

def move_xr():
    move()
    move()
    move()

if __name__ == "__main__":
    main()
