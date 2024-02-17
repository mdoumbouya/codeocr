from stanfordkarel import *
# Karel should fill the whole world with beepers.

def main():
# You should write your code to make Karel do its task in this function
# Make sure to delete the 'pass' line before starting to write your own code. 
# You should also delete this comment and replace it with a better more descriptive one.
while not left_is_blocked():
    put_beeper_line()
    reset_position()
put_beeper_line()

def put_beeper_line():
put_beeper()
while front_is_clear():
    move()
    put_beeper()
