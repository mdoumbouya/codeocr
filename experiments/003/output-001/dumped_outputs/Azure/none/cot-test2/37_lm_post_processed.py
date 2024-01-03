from karel.stanfordkarel import *

def main ():
build_column ( )
step_up ( )
build_column ()
step_up()
build_column ( )
step_up()
build_column ()

def build_column ( ) :
turn_left ( )
build_beeper ( )
build_beeper ( )
build_beeper ( )
build_beeper ( )
put_beeper ()
go_back ()
turn_left ( )

def build_beeper ( ):
put_beeper ( )
move ()

def go_back ():
turn_around ( )
step_up ()

def turn_around ( ) :
turn_left ()
turn_left ()

def step_up():
move ( )
move ( )
move ( )
move ( )

if __name__ == "__main__":
main ( )
