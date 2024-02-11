#karel needs to move to the bottom of the next arch to commenc.
#hence building the next column.
#Precondition: karel is facing east
#Post-condition: karel is facing east at the next column site.

def move_to_next_arch_bottom():
    if front_is_clear():
        for i in range(4):
            move()

def turn_around():
    turn_left()
    turn_left()
    turn_left()
if __name__ == '__main__':
    main()
