from karel.stanfordkarel import *

def main():
    move()
    move()
    turn_right()
    move()
    turn_left()
    move()
    pick_beeper()
    return_home()

def return_home():
    turn_around()
    move()
    turn_right()
    move()
    turn_left()
    move()
    move()
    turn_around()

def turn_right():
    for i in range(3):
        turn_left()

def turn_around():
    for i in range(2):
        turn_left()
if __name__ == '__main__':
    main()
