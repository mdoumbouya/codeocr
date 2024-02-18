from karel.stanfordkarel import *

def main():
    turn_left()
    move_N()
    turne_SC()
    move_X()
    turn_left()
    move_N()
    turne_SC()

def turne_SC():
    turn_3x()
    move()
    turn_left()

def turne_N():
    turn()
    turn_3x()
    move_X()

def move_X():
    move()
    move()
    move()

def move_C():
    for i in rang(5):
        if front_is_clear():
            put_beeper()
            move()
        else:
            put_beeper()

def turn_3x():
    turn_left()
    turn_left()
    turn_left()

def move_arc():
    move()
    move()
    move()
    move()

if __name__ == "__main__":
    main()
