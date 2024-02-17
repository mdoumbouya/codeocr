#karel needs to move to the bottom of the next notch to come
#Hence building the next column.
# Precondition: Karel is facing east
# post-condition: Karel is facing east at the next column site.

def move_to_next_notch_bottom():
if front_is_clear():
for i in range (4) :
move ()

def turn_around():
turn_left ()
turn_left ()

if __name__ == "__main__":
main ()
