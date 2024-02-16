from karel.stanfordkarel import *

def main():
get_out()
pick_food()
get_back_home()

def get_out():
turn_right()
move()
turn_left()
move()
move()
move()

def pick_food():
pick_beeper()
turn_around()

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
