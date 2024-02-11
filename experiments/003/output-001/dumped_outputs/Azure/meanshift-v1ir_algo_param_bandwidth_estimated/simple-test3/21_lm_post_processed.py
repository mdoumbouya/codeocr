from stanfordkarel import *

def main():
    while not left_is_blocked():
        put_beeper_line()
        reset_position()
        put_beeper_line()

def put_beeper_line():
    put_beeper()
    while front_is_clear():
        move()
        put_beeper()
