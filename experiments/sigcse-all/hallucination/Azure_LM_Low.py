#0


num = int(input("Enter a number: "))
Ans = 1
while num > 1:
    Ans *= num
    num -= 1
print(Ans)


#1


from karel.stanfordkarel import *

# This program makes Karel pick up
# a beeper and go back into her house.
def main():
    # Move to the beeper.
    move_beeper()
    # Pick the beeper up.
    pick_beeper()
    # Return to Karel's starting point.
    go_back()


# This function moves karel to the beeper.
def move_beeper():
    for i in range(2):
        move()
        turn_right()
        move()
        turn_left()
        move()


# this function return to Karel's starting point
def go_back():
    for i in range(2):
        turn_left()
        for i in range(3):
            move()
        turn_right()
        move()
        turn_right()


def turn_right():
    for i in range(3):
        turn_left()


if __name__ == "__main__":
    main()


#2


def main():
    my_word = input("Enter the original word: ")
    # Function calling
    reversed_word = reverse(my_word)
    print("The reversed word is: " + reversed_word)


# Helper Function
def reverse(word):
    # reversed - word
    new_word = ""
    # A char by char
    for char in word:
        new_word = char + new_word
    # return
    return new_word


if __name__ == "__main__":
    main()


#3


input_number = int(input("Enter number"))
val = input_number
result = input_number
while val > 1:
    val = val - 1
    result = result * val
print("factorial of " + str(input_number) + " is " + str(result))


#4


def main():
    num = input("Input: ")
    sum = 0
    for n in num:
        sum += int(n)
    print(sum)


#5


def main():
    num = input("enter the number you want to add: ")
    Sum = 0
    for i in str(num):
        Sum = Sum + int(i)
    print("sum of the values you entered is", Sum)


#6


user_input = input("write your string here: ")
Upper = user_input.upper()
print(Upper)


#7


.python
from karel.stanfordkarel import *

# Karel should fill the world with beepers.
def main():
    # decomposition using a function name for
    # each associated activity
    while left_is_clear():
        fill_one_row()
        return_to_row_start()
        move_up()
    # rewrite code after while loop to overcome
    # fencepost bug
    fill_one_row()


#8


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


if __name__ == "__main__":
    main()


#9


def main():
    vowel_count = 0
    vowels = ["a", "e", "i", "o", "u"]
    input_string = input("Enter the string:")
    input_string = input_string.lower()
    for char in input_string:
        for vowel in vowels:
            if char == vowel:
                vowel_count += 1
    print(vowel_count)


if __name__ == "__main__":
    main()


#10


def main():
    string = str(input("Enter string: "))
    for i in range((len(string) - 1), -1, -1):
        print(string[i])


#11


seq = [1, 2, 3, 4, 5, 6, 7, 8, 9]
seq_even = []
# It checks every element in list (sequence) - --
for i in seq:
    # it decides whether an element from sequence is even --.
    if i % 2 == 0:
        seq_even.append(i)  # appends even ; in empty list (seq_even)
print(seq_even)


#12


from graphics import Canvas

canvas_width = 300
canvas_height = 300
circle_size = 20
delay = 0.01


def main():
    canvas = Canvas(canvas_width, canvas_height)
    while True:
        mouse_x = canvas.get_mouse_x()
        mouse_y = canvas.get_mouse_y()
        if (
            mouse_x >= 0
            and mouse_x <= canvas_width
            and mouse_y >= 0
            and mouse_y <= canvas_height
        ):
            pass


#13


# 1 karel Problem - Karel home
from karel.stanfordkarel import *

# This program defines a main function which should make karel
# move to the beeper, pick it up and return home
def main():
    get_out()
    pick_food()
    get_back_home()


# pre: Karel facing east, at the corner of starting position
# post: karel facing east, outside the home, at the position of beeper
def get_out():
    turn_right()
    move()
    turn_left()
    move()
    move()
    move()


# post: Karel facing west, at the position of beeper
def pick_food():
    pick_beeper()
    turn_around()


# post: Karel facing east, at the corner of starting position
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


if __name__ == "__main__":
    main()


#14


def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


print(factorial(5))


#15


def main():
    list1 = [1, 2, 3, 4]
    list2 = [3, 4, 5, 6]
    List = []
    for elem1 in list1:
        for elem2 in list2:
            if elem1 == elem2:
                List.append(elem2)
    print(List)


main()


#16


String = input()
print(String[::-1])


#17


from karel.stanfordkarel import *


def main():
    turn_left()
    tower_N()
    tower_SC()
    move_4x()
    turn_left()
    tower_N()
    tower_SC()
    del tower_s()
    turn_3x()
    Tower()
    turn_left()
    del tower_NC()
    Tower()
    turn_3x()
    move_4x()
    del tower()
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


if __name__ == "__main__":
    main()


#18


def main():
    string = str(input("Enter string: "))
    for i in range((len(string) - 1), -1, -1):
        print(string[i])


if __name__ == "__main__":
    main()


#19


def main():
    num = int(input("Enter a num: "))
    if is_prime(num):
        print(f"Num is prime")
    else:
        print("Num is not prime")


def is_prime(n):
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


if __name__ == "__main__":
    main()


#20


from karel.stanfordkarel import *


def main():
    turn_left()
    while front_is_clear():
        turn_right()
        fill_row()
        return_to_home()
        jump_row()
        turn_right()
        fill_row()
        return_to_home()
    while front_is_clear():
        move()

    def fill_row():
        while front_is_clear():
            put_beeper()
            move()
        put_beeper()


#21


from stanfordkarel import *

# Karel should fill the whole world with beepers.


def main():
    # You should write your code to make Karel do its task in this function.
    # Make sure to delete the 'pass' line before starting to write your own code.
    # You should also delete this comment and replace it with a better, more descriptive one.

    while not left_is_blocked():
        put_beeper_line()
        reset_position()
        put_beeper_line()


def put_beeper_line():
    put_beeper()
    while front_is_clear():
        move()
        put_beeper()


#22


# Karel needs to move to the bottom of the next notch to come
# Hence building the next column.
# Precondition: Karel is facing east
# post-condition: Karel is facing east at the next column site.
def move_to_next_arch_bottom():
    if front_is_clear():
        for i in range(4):
            move()


def turn_around():
    turn_left()
    turn_left()


if __name__ == "__main__":
    main()


#23


def find_largest_smallest(numbers):
    if not numbers:
        return None
    smallest = largest = numbers[0]
    for num in numbers:
        if num < smallest:
            smallest = num
        if num > largest:
            largest = num
    return smallest, largest


# Example usage:
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
result = find_largest_smallest(numbers)
print(result)


#24


def main():
    user_number = input("Enter the number:\n")
    result = sum_of_digits(user_number)
    print("The sum of the digits is ", result)


def sum_of_digits(user_number):
    number_str = str(user_number)
    digit_sum = 0
    for digit in number_str:
        digit_sum += int(digit)
    return digit_sum


if __name__ == "__main__":
    main()


#25


def is_prime(n):
    """
    Returns True if n is prime, False otherwise
    """
    if n <= 1:
        return False
    for i in range(2, int(n * 0.5) + 1):
        if n % i == 0:
            return False
    return True


def main():
    """
    The main function.
    """
    n = int(input("Enter a number: "))
    if is_prime(n):
        print(n, "is a prime number.")
    else:
        print(n, "is not a prime number.")


if __name__ == "__main__":
    main()


#26


# Reverse String
def main():
    str = input("Input a string: ")
    r_str = ""
    for i in str:
        r_str = i + r_str
    print(r_str)


if __name__ == "__main__":
    main()


#27


# Write a Python program to find the longest word in a given text
def main():
    sentence = input("Input a sentence: ")
    list = sentence.split()
    Lword = ""
    for word in list:
        if len(word) > len(Lword):
            Lword = word
    print(Lword)


if __name__ == "__main__":
    main()


#28


def greatest_common_divisor(a, b):
    smaller_number = a if a < b else b
    common_divisor = []
    for i in range(1, smaller_number + 1):
        if a % i == 0 and b % i == 0:
            common_divisor.append(i)
    return common_divisor[-1]


#29


def main():
    # The program should determine whether the given year is a leap year
    # (divisible by 4, divisible by 100 but also by 400).
    print("This program will help you identify if a given year is a leap year or not.")
    print(" ")
    identify_a_leap_year()
    ask_for_a_new_year_to_identify()


def identify_a_leap_year():
    print("Please input a year below (in number form).")
    Year = int(input("Year: "))
    print(" ")
    if (Year % 4 == 0) and (Year % 100 != 0 or Year % 400 == 0):
        print("The Year " + str(Year) + " is a leap year.")
    else:
        print("The Year " + str(Year) + " is not a leap year.")


def ask_for_a_new_year_to_identify():
    while True:
        print(" ")
        ask = input("Do you want to identify a new year? Yes/No: ")
        print(" ")
        if ask == "Yes" or ask == "yes":
            identify_a_leap_year()
        elif ask == "No" or ask == "no":
            print("Thank you. See you again!")
            break
        elif ask != "Yes" and ask != "yes" and ask != "No" and ask != "no":
            print("Wrong keyword. Please type the exact keyword.")


if __name__ == "__main__":
    main()


#30


Sum = 0
number = input()
for i in number:
    Sum += int(i)
print(Sum)


#31


def factorial(n):
    if n <= 1:
        return 1
    else:
        return factorial(n - 1) * n


print(factorial(int(input())))


#32


year = int(input())
if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
    print(True)
else:
    print(False)


#33


word = input()
word = "".join([i for i in word])
print(word)


#34


list1 = [1, 2, 3, 4]
list2 = [3, 4, 5, 6]
list3 = [i for i in list1 if i in list2]
print(list3)


#35


list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
even = [i for i in list1 if i % 2 == 0]
print(even)


#36


def main():
    year = int(input())
    if year % 4 == 0 and year % 100 != 0:
        print("True")
    elif year % 100 == 0 and year % 400 == 0:
        print("True")
    else:
        print("False")


if __name__ == "__main__":
    main()


#37


from karel.stanfordkarel import *


def main():
    build_column()
    step_up()
    build_column()
    step_up()
    build_column()
    step_up()
    build_column()


def build_column():
    turn_left()
    build_beeper()
    build_beeper()
    build_beeper()
    build_beeper()
    put_beeper()
    go_back()
    turn_left()


def build_beeper():
    put_beeper()
    move()


def go_back():
    turn_around()
    step_up()


def turn_around():
    turn_left()
    turn_left()


def step_up():
    move()
    move()
    move()
    move()


if __name__ == "__main__":
    main()


#38


def main():
    input_string = input("Input string:")
    ret = " "
    for ch in input_string:
        ret = ret + ch.upper()
    print(ret)


if __name__ == "__main__":
    main()


#39


from Karel.StanfordKarel import *


def main():
    move_to_beeper()
    pick_beeper()
    turn_around()
    return_to_start()


def move_to_beeper():
    while front_is_clear():
        move()
    turn_right()
    move()
    turn_left()
    move()


def turn_around():
    turn_left()
    turn_left()


#40


from karel.stanfordkarel import *


def main():
    while front_is_clear():
        build_tower()


def build_tower():
    while front_is_clear():
        put_beeper()
        move()
        put_beeper()
        column_return()


def column_return():
    while front_is_blocked():
        turn_around()
    while front_is_clear():
        move()
    next_tower()


def turn_around():
    for i in range(2):
        turn_left()


def next_tower():
    if right_is_clear():
        turn_right()
        move()
        turn_right()
    else:
        turn_around()
    while front_is_clear():
        move()


def turn_right():
    for i in range(3):
        turn_left()


if __name__ == "__main__":
    main()


#41


def filter_string_a(string):
    string.sort()
    filtered_string_list = []
    for stru in string:
        if stru.startswith("a"):
            filtered_string_list.append(stru)
    return filtered_string_list


input_string = ["apple", "banana", "avocado", "chewing", "apricot"]
output = filter_string_a(input_string)
print(output)


#42


def main():
    while front_is_clear():
        move()
    if front_is_blocked():
        turn_around()
        move()
        turn_left()
        move()
        pick_beeper()
        turn_left()
        turn_left()
    while front_is_clear():
        move()
    if front_is_blocked():
        turn_around()
        move()
        turn_around()


def turn_around():
    for i in range(3):
        left()


#43


def is_leap_year(year):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


def main():
    year = int(input("Enter a year: "))
    is_leap = is_leap_year(year)
    print(is_leap)


if __name__ == "__main__":
    main()


#44


def main():
    print("problem - 5")
    numb = int(input("write an integer number: "))
    mak_list = [int(x) for x in str(numb)]
    add_numb = 0
    for i in mak_list:
        add_numb += i
    print("Sum of the number's: ", add_numb)


if __name__ == "__main__":
    main()


#45


num = int(input("Enter a number: "))
Ans = 1
while num > 1:
    Ans *= num
    num -= 1
print(Ans)


#46


from karel.stanfordkarel import *

# This program makes Karel pick up
# a beeper and go back into her house.
def main():
    # Move to the beeper.
    move_beeper()
    # Pick the beeper up.
    pick_beeper()
    # Return to Karel's starting point.
    go_back()


# This function moves karel to the beeper.
def move_beeper():
    for i in range(2):
        move()
        turn_right()
        move()
        turn_left()
        move()


# this function return to Karel's starting point
def go_back():
    for i in range(2):
        turn_left()
    for i in range(3):
        move()
        turn_right()
        move()
        turn_right()


def turn_right():
    for i in range(3):
        turn_left()


if __name__ == "__main__":
    main()


#47


def main():
    my_word = input("Enter The original word: ")
    # Function calling
    reversed_word = reverse(my_word)
    print("The reversed word is: " + reversed_word)


# Helper Function
def reverse(word):
    # reversed - word
    new_word = ""
    # A char by char
    for char in word:
        new_word = char + new_word
    # return
    return new_word


if __name__ == "__main__":
    main()


#48


input_number = int(input("Enter number"))
val = input_number
result = input_number
while val > 1:
    val = val - 1
    result = result * val
print("factorial of " + str(input_number) + " is " + str(result))


#49


def main():
    num = input("Input: ")
    sum = 0
    for n in num:
        sum += int(n)
    print(sum)


#50


def main():
    num = input("enter the number you want to add: ")
    Sum = 0
    for i in str(num):
        Sum = Sum + int(i)
    print("sum of the values you entered is", Sum)


#51


user_input = input("write your string here: ")
Upper = user_input.upper()
print(Upper)


#52


from karel.stanfordkarel import *

# Karel should fill the world with beepers.
def main():
    # decomposition using a function name for
    # each associated activity
    while left_is_clear():
        fill_one_row()
        return_to_row_start()
        move_up()
    # rewrite code after while loop to overcome
    # fencepost bug
    fill_one_row()


#53


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


if __name__ == "__main__":
    main()


#54


def main():
    vowel_count = 0
    vowels = ["a", "e", "i", "o", "u"]
    input_string = input("Enter the string:")
    input_string = input_string.lower()
    for char in input_string:
        for vowel in vowels:
            if char == vowel:
                vowel_count += 1
    print(vowel_count)


if __name__ == "__main__":
    main()


#55


def main():
    string = str(input("Enter string: "))
    for i in range((len(string) - 1), -1, -1):
        print(string[i])


#56


seq = [1, 2, 3, 4, 5, 6, 7, 8, 9]
seq_even = []
# It checks every element in list (sequence) - --
for i in seq:
    # it decides whether an element from sequence is even --.
    if i % 2 == 0:
        seq_even.append(i)  # appends even ; in empty list (seq_even)
print(seq_even)


#57


from graphics import Canvas

CANVAS_WIDTH = 300
CANVAS_HEIGHT = 300
CIRCLE_SIZE = 20
DELAY = 0.01


def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    while True:
        MOUSE_X = canvas.get_mouse_x()
        MOUSE_Y = canvas.get_mouse_y()
        if (
            MOUSE_X >= 0
            and MOUSE_X <= CANVAS_WIDTH
            and MOUSE_Y >= 0
            and MOUSE_Y <= CANVAS_HEIGHT
        ):
            pass


#58


# 1 karel Problem - Karel home
from karel.stanfordkarel import *

# This program defines a main function which should make karel
# move to the beeper, pick it up and return home
def main():
    get_out()
    pick_food()
    get_back_home()


# pre: Karel facing east, at the corner of starting position
# post: karel facing east, outside the home, at the position of beeper
def get_out():
    turn_right()
    move()
    turn_left()
    move()
    move()
    move()


# post: Karel facing west, at the position of beeper
def pick_food():
    pick_beeper()
    turn_around()


# post: Karel facing east, at the corner of starting position
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


if __name__ == "__main__":
    main()


#59


def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


print(factorial(5))


#60


def main():
    list1 = [1, 2, 3, 4]
    list2 = [3, 4, 5, 6]
    List = []
    for elem1 in list1:
        for elem2 in list2:
            if elem1 == elem2:
                elem = elem2
                List.append(elem)
    print(List)

    return


#61


String = input()
print(String[::-1])


#62



from karel.stanfordkarel import *

def main():
    turn_left()
    tower_N()
    tower_SC()
    move_4x()
    turn_left()
    tower_N()
    tower_SC()
    del tower_s():
    turn_3x()
    Tower()
    turn_left()
    del tower_NC():
    Tower()
    turn_3x()
    move_4x()
    del tower():
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

if __name__ == "__main__":
    main()


#63


def main():
    string = str(input("Enter string: "))
    for i in range((len(string) - 1), -1, -1):
        print(string[i])


if __name__ == "__main__":
    main()


#64


def main():
    num = int(input("Enter a num:"))
    if is_prime(num):
        print(f"Num is prime")
    else:
        print("Not prime")


def is_prime(n):
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    for i in range(5, int(n**0.5) + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True


if __name__ == "__main__":
    main()


#65


from karel.stanfordkarel import *


def main():
    turn_left()
    while front_is_clear():
        turn_right()
        fill_row()
        return_to_home()
        jump_row()
        turn_right()
        fill_row()
        return_to_home()
    while front_is_clear():
        move()

    def fill_row():
        while front_is_clear():
            put_beeper()
            move()
        put_beeper()


#66


from stanfordkarel import *

# Karel should fill the whole world with beepers.


def main():
    # You should write your code to make Karel do its task in this function.
    # Make sure to delete the 'pass' line before starting to write your own code.
    # You should also delete this comment and replace it with a better, more descriptive one.

    while not left_is_blocked():
        put_beeper_line()
        reset_position()
        put_beeper_line()


def put_beeper_line():
    put_beeper()
    while front_is_clear():
        move()
        put_beeper()


#67


# Karel needs to move to the bottom of the next notch to come
# Hence building the next column.
# Precondition: Karel is facing east
# post-condition: Karel is facing east at the next column site.
def move_to_next_arch_bottom():
    if front_is_clear():
        for i in range(4):
            move()


def turn_around():
    turn_left()
    turn_left()


if __name__ == "__main__":
    main()


#68


def find_largest_smallest(numbers):
    if not numbers:
        return None
    smallest = largest = numbers[0]
    for num in numbers:
        if num < smallest:
            smallest = num
        if num > largest:
            largest = num
    return smallest, largest


# Example usage:
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
result = find_largest_smallest(numbers)
print(result)


#69


def main():
    user_number = input("Enter the number:\n")
    result = sum_of_digits(user_number)
    print("The sum of the digits is ", result)


def sum_of_digits(user_number):
    number_str = str(user_number)
    digit_sum = 0
    for digit in number_str:
        digit_sum += int(digit)
    return digit_sum


if __name__ == "__main__":
    main()


#70


def is_prime(n):
    """
    Returns True if n is prime, False otherwise
    """
    if n <= 1:
        return False
    for i in range(2, int(n * 0.5) + 1):
        if n % i == 0:
            return False
    return True


def main():
    """
    The main function.
    """
    n = int(input("Enter a number: "))
    if is_prime(n):
        print(n, "is a prime number.")
    else:
        print(n, "is not a prime number.")


if __name__ == "__main__":
    main()


#71


# Reverse String
def main():
    str = input("Input a string: ")
    rev_str = ""
    for i in str:
        rev_str = i + rev_str
    print(rev_str)


if __name__ == "__main__":
    main()


#72


# Write a Python program to find the longest word in a given text
def main():
    sentence = input("Input a sentence: ")
    list = sentence.split()
    Lword = ""
    for word in list:
        if len(word) > len(Lword):
            Lword = word
    print(Lword)


if __name__ == "__main__":
    main()


#73


def greatest_common_divisor(a, b):
    smaller_number = a if a < b else b
    common_divisor = []
    for i in range(1, smaller_number + 1):
        if a % i == 0 and b % i == 0:
            common_divisor.append(i)
    return common_divisor[-1]


#74


def main():
    # The program should determine whether the given year is a leap year
    # (divisible by 4, divisible by 100 but also by 400).
    print("This program will help you identify if a given year is a leap year or not.")
    print(" ")
    identify_a_leap_year()
    ask_for_a_new_year_to_identify()


def identify_a_leap_year():
    print("Please input a year below (in number form).")
    Year = int(input("Year: "))
    print(" ")
    if (Year % 4 == 0) and (Year % 100 != 0 or Year % 400 == 0):
        print("The Year " + str(Year) + " is a leap year.")
    else:
        print("The Year " + str(Year) + " is not a leap year.")


def ask_for_a_new_year_to_identify():
    while True:
        print(" ")
        ask = input("Do you want to identify a new year? Yes/No: ")
        print(" ")
        if ask == "Yes" or ask == "yes":
            identify_a_leap_year()
        elif ask == "No" or ask == "no":
            print("Thank you. See you again!")
            break
        elif ask != "Yes" and ask != "yes" and ask != "No" and ask != "no":
            print("Wrong keyword. Please type the exact keyword.")


if __name__ == "__main__":
    main()


#75


Sum = 0
number = input()
for i in number:
    Sum += int(i)
print(Sum)


#76


def factorial(n):
    if n <= 1:
        return 1
    else:
        return factorial(n - 1) * n


print(factorial(int(input())))


#77


year = int(input())
if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
    print(True)
else:
    print(False)


#78


word = input()
word = "".join([i for i in word[::-1]])
print(word)


#79


list1 = [1, 2, 3, 4]
list2 = [3, 4, 5, 6]
list3 = [i for i in list1 if i in list2]
print(list3)


#80


list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
even = [i for i in list1 if i % 2 == 0]
print(even)


#81


def main():
    year = int(input())
    if year % 4 == 0 and year % 100 != 0:
        print("True")
    elif year % 100 == 0 and year % 400 == 0:
        print("True")
    else:
        print("False")


if __name__ == "__main__":
    main()


#82


from karel.stanfordkarel import *


def main():
    build_column()
    step_up()
    build_column()
    step_up()
    build_column()
    step_up()
    build_column()


def build_column():
    turn_left()
    build_beeper()
    build_beeper()
    build_beeper()
    build_beeper()
    put_beeper()
    go_back()
    turn_left()


def build_beeper():
    put_beeper()
    move()


def go_back():
    turn_around()
    step_up()


def turn_around():
    turn_left()
    turn_left()


def step_up():
    move()
    move()
    move()
    move()


if __name__ == "__main__":
    main()


#83


def main():
    input_string = input("Input string:")
    ret = " "
    for ch in input_string:
        ret = ret + ch.upper()
    print(ret)


if __name__ == "__main__":
    main()


#84


from Karel.StanfordKarel import *


def main():
    move_to_beeper()
    pick_beeper()
    turn_around()
    return_to_start()


def move_to_beeper():
    while front_is_clear():
        move()
    turn_right()
    move()
    turn_left()
    move()


def turn_around():
    turn_left()
    turn_left()


#85


from karel.stanfordkarel import *


def main():
    while front_is_clear():
        build_tower()


def build_tower():
    while front_is_clear():
        put_beeper()
        move()
    put_beeper()
    column_return()


def column_return():
    while front_is_blocked():
        turn_around()
    while front_is_clear():
        move()
    next_tower()


def turn_around():
    for i in range(2):
        turn_left()


def next_tower():
    if right_is_clear():
        turn_right()
        move()
        turn_right()
    else:
        turn_around()
        while front_is_clear():
            move()


def turn_right():
    for i in range(3):
        turn_left()


if __name__ == "__main__":
    main()


#86


def filter_string_a(string):
    string.sort()
    filtered_string_list = []
    for stru in string:
        if stru.startswith("a"):
            filtered_string_list.append(stru)
    return filtered_string_list


input_string = ["apple", "banana", "avocado", "chewing", "apricot"]
output = filter_string_a(input_string)
print(output)


#87


def main():
    while front_is_clear():
        move()
    if front_is_blocked():
        turn_around()
        move()
        turn_left()
        move()
        pick_beeper()
        turn_left()
        turn_left()
    while front_is_clear():
        move()
    if front_is_blocked():
        turn_around()
        move()
        turn_around()


def turn_around():
    for i in range(3):
        left()


#88


def is_leap_year(year):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


def main():
    year = int(input("Enter a year: "))
    is_leap = is_leap_year(year)
    print(is_leap)


if __name__ == "__main__":
    main()


#89


def main():
    print("problem - 5")
    numb = int(input("write an integer number: "))
    mak_list = [int(x) for x in str(numb)]
    add_numb = 0
    for i in mak_list:
        add_numb += i
    print("Sum of the number's digits: ", add_numb)


if __name__ == "__main__":
    main()


#90


num = int(input("Enter a number: "))
Ans = 1
while num > 1:
    Ans *= num
    num -= 1
print(Ans)


#91


from karel.stanfordkarel import *

# This program makes Karel pick up
# a beeper and go back into her house.
def main():
    # Move to the beeper.
    move_beeper()
    # Pick the beeper up.
    pick_beeper()
    # Return to Karel's starting point.
    go_back()


# This function moves karel to the beeper.
def move_beeper():
    for i in range(2):
        move()
        turn_right()
        move()
        turn_left()
        move()


# this function return to Karel's starting point
def go_back():
    for i in range(2):
        turn_left()
    for i in range(3):
        move()
        turn_right()
        move()
        turn_right()


def turn_right():
    for i in range(3):
        turn_left()


if __name__ == "__main__":
    main()


#92


def main():
    my_word = input("Enter the original word: ")
    # Function calling
    reversed_word = reverse(my_word)
    print("The reversed word is: " + reversed_word)


# Helper Function
def reverse(word):
    # reversed word
    new_word = ""
    # char by char
    for char in word:
        new_word = char + new_word
    # return
    return new_word


if __name__ == "__main__":
    main()


#93


input_number = int(input("Enter number"))
val = input_number
result = input_number
while val > 1:
    val = val - 1
    result = result * val
print("factorial of " + str(input_number) + " is " + str(result))


#94


def main():
    num = input("Input: ")
    sum = 0
    for n in num:
        sum += int(n)
    print(sum)


#95


def main():
    num = input("Enter the number you want to add: ")
    Sum = 0
    for i in str(num):
        Sum = Sum + int(i)
    print("Sum of the value you entered is", Sum)


#96


user_input = input("write your string here: ")
Upper = user_input.upper()
print(Upper)


#97


from karel.stanfordkarel import *

# Karel should fill the world with beepers.
def main():
    # decomposition using a function name for
    # each associated activity
    while left_is_clear():
        fill_one_row()
        return_to_row_start()
        move_up()
    # rewrite code after while loop to overcome
    # fencepost bug
    fill_one_row()


#98


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


if __name__ == "__main__":
    main()


#99


def main():
    vowel_count = 0
    vowels = ["a", "e", "i", "o", "u"]
    input_string = input("Enter the string:")
    input_string = input_string.lower()
    for char in input_string:
        for vowel in vowels:
            if char == vowel:
                vowel_count += 1
    print(vowel_count)


if __name__ == "__main__":
    main()


#100


def main():
    string = str(input("Enter string: "))
    for i in range((len(string) - 1), -1, -1):
        print(string[i])


#101


seq = [1, 2, 3, 4, 5, 6, 7, 8, 9]
seq_even = []
# It checks every element in list (sequence) - --
for i in seq:
    # it decides whether an element from sequence is even --.
    if i % 2 == 0:
        seq_even.append(i)  # appends even ; in empty list (seq_even)
print(seq_even)


#102


from graphics import Canvas

CANVAS_WIDTH = 300
CANVAS_HEIGHT = 300
CIRCLE_SIZE = 20
DELAY = 0.01


def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    while True:
        MOUSE_X = canvas.get_mouse_x()
        MOUSE_Y = canvas.get_mouse_y()
        if (
            MOUSE_X >= 0
            and MOUSE_X <= CANVAS_WIDTH
            and MOUSE_Y >= 0
            and MOUSE_Y <= CANVAS_HEIGHT
        ):
            continue


#103


# 1 karel Problem - Karel home
from karel.stanfordkarel import *

# This program defines a main function which should make karel
# move to the beeper, pick it up and return home
def main():
    get_out()
    pick_food()
    get_back_home()


# pre: Karel facing east, at the corner of starting position
# post: karel facing east, outside the home, at the position of beeper
def get_out():
    turn_right()
    move()
    turn_left()
    move()
    move()
    move()


# post: Karel facing west, at the position of beeper
def pick_food():
    pick_beeper()
    turn_around()


# post: Karel facing east, at the corner of starting position
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


if __name__ == "__main__":
    main()


#104


def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


print(factorial(5))


#105


def main():
    list1 = [1, 2, 3, 4]
    list2 = [3, 4, 5, 6]
    List = []
    for elem1 in list1:
        for elem2 in list2:
            if elem1 == elem2:
                elem = elem2
                List.append(elem)
    print(List)

    return


#106


String = input()
print(String[::-1])


#107



from karel.stanfordkarel import *

def main():
    turn_left()
    tower_N()
    tower_SC()
    move_4x()
    turn_left()
    tower_N()
    tower_SC()
    del tower_s():
    turn_3x()
    Tower()
    Turn_left()
    del tower_NC()
    Tower()
    turn_3x()
    move_4x()
    del tower():
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

if __name__ == "__main__":
    main()


#108


def main():
    string = str(input("Enter string: "))
    for i in range((len(string) - 1), -1, -1):
        print(string[i])


if __name__ == "__main__":
    main()


#109


def main():
    num = int(input("Enter a num: "))
    if is_prime(num):
        print(f"Num is prime")
    else:
        print("Num is not prime")


def is_prime(n):
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    for i in range(5, int(n**0.5) + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True


if __name__ == "__main__":
    main()


#110


from karel.stanfordkarel import *


def main():
    turn_left()
    while front_is_clear():
        turn_right()
        fill_row()
        return_to_home()
        jump_row()
        turn_right()
        fill_row()
        return_to_home()
    while front_is_clear():
        move()

    def fill_row():
        while front_is_clear():
            put_beeper()
            move()
        put_beeper()


#111


from stanfordkarel import *

# Karel should fill the whole world with beepers.


def main():
    # You should write your code to make Karel do its task in this function.
    # Make sure to delete the 'pass' line before starting to write your own code.
    # You should also delete this comment and replace it with a better, more descriptive one.

    while not left_is_blocked():
        put_beeper_line()
        reset_position()
        put_beeper_line()


def put_beeper_line():
    put_beeper()
    while front_is_clear():
        move()
        put_beeper()


#112


# Karel needs to move to the bottom of the next arch to come
# Hence building the next column.
# Precondition: Karel is facing east
# post-condition: Karel is facing east at the next column site.
def move_to_next_arch_bottom():
    if front_is_clear():
        for i in range(4):
            move()


def turn_around():
    turn_left()
    turn_left()


if __name__ == "__main__":
    main()


#113


def find_largest_smallest(numbers):
    if not numbers:
        return None
    smallest = largest = numbers[0]
    for num in numbers:
        if num < smallest:
            smallest = num
        if num > largest:
            largest = num
    return smallest, largest


# Example usage:
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
result = find_largest_smallest(numbers)
print(result)


#114


def main():
    user_number = input("Enter the number: ")
    result = sum_of_digits(user_number)
    print("The sum of the digits is ", result)


def sum_of_digits(user_number):
    number_str = str(user_number)
    digit_sum = 0  # zero
    for digit in number_str:
        digit_sum += int(digit)
    return digit_sum


if __name__ == "__main__":
    main()


#115


def is_prime(n):
    """
    Returns True if n is prime, False otherwise
    """
    if n <= 1:
        return False
    for i in range(2, int(n * 0.5) + 1):
        if n % i == 0:
            return False
    return True


def main():
    """
    The main function.
    """
    n = int(input("Enter a number: "))
    if is_prime(n):
        print(n, "is a prime number.")
    else:
        print(n, "is not a prime number.")


if __name__ == "__main__":
    main()


#116


# Reverse String
def main():
    str = input("Input a string: ")
    r_str = ""
    for i in str:
        r_str = i + r_str
    print(r_str)


if __name__ == "__main__":
    main()


#117


# Write a Python program to find the longest word in a given text
def main():
    sentence = input("Input a sentence: ")
    list = sentence.split()
    Lword = ""
    for word in list:
        if len(word) > len(Lword):
            Lword = word
    print(Lword)


if __name__ == "__main__":
    main()


#118


def greatest_common_divisor(a, b):
    smaller_number = a if a < b else b
    common_divisor = []
    for i in range(1, smaller_number + 1):
        if a % i == 0 and b % i == 0:
            common_divisor.append(i)
    return common_divisor[-1]


#119


def main():
    # The program should determine whether the given year is a leap year
    # (divisible by 4, divisible by 100 but also by 400).
    print("This program will help you identify if a given year is a leap year or not.")
    print(" ")
    identify_a_leap_year()
    ask_for_a_new_year_to_identify()


def identify_a_leap_year():
    print("Please input a year below (in number form).")
    Year = int(input("Year: "))
    print(" ")
    if (Year % 4 == 0) or (Year % 100 == 0) or (Year % 400 == 0):
        print("The Year " + str(Year) + " is a leap year.")
    else:
        print("The Year " + str(Year) + " is not a leap year.")


def ask_for_a_new_year_to_identify():
    while True:
        print(" ")
        ask = input("Do you want to identify a new year? Yes/No: ")
        print(" ")
        if ask == "Yes" or ask == "yes":
            identify_a_leap_year()
        elif ask == "No" or ask == "no":
            print("Thank you. See you again!")
            break
        elif ask != "Yes" or ask != "yes" or ask != "No" or ask != "no":
            print("Wrong keyword. Please type the exact keyword.")


if __name__ == "__main__":
    main()


#120


Sum = 0
number = input()
for i in number:
    Sum += int(i)
print(Sum)


#121


def factorial(n):
    if n <= 1:
        return 1
    else:
        return factorial(n - 1) * n


print(factorial(int(input())))


#122


year = int(input())
if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
    print(True)
else:
    print(False)


#123


word = input()
word = "".join([i for i in word])
print(word)


#124


list1 = [1, 2, 3, 4]
list2 = [3, 4, 5, 6]
list3 = [i for i in list1 if i in list2]
print(list3)


#125


list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
even = [i for i in list1 if i % 2 == 0]
print(even)


#126


def main():
    year = int(input())
    if year % 4 == 0 and year % 100 != 0:
        print("True")
    elif year % 100 == 0 and year % 400 == 0:
        print("True")
    else:
        print("False")


if __name__ == "__main__":
    main()


#127


from karel.stanfordkarel import *


def main():
    build_column()
    step_up()
    build_column()
    step_up()
    build_column()
    step_up()
    build_column()


def build_column():
    turn_left()
    build_beeper()
    build_beeper()
    build_beeper()
    build_beeper()
    put_beeper()
    go_back()
    turn_left()


def build_beeper():
    put_beeper()
    move()


def go_back():
    turn_around()
    step_up()


def turn_around():
    turn_left()
    turn_left()


def step_up():
    move()
    move()
    move()
    move()


if __name__ == "__main__":
    main()


#128


def main():
    input_string = input("Input string:")
    ret = " "
    for ch in input_string:
        ret = ret + ch.upper()
    print(ret)


if __name__ == "__main__":
    main()


#129


from Karel.StanfordKarel import *


def main():
    move_to_beeper()
    pick_beeper()
    turn_around()
    return_to_start()


def move_to_beeper():
    while front_is_clear():
        move()
    turn_right()
    move()
    turn_left()
    move()


def turn_around():
    turn_left()
    turn_left()


#130


from karel.stanfordkarel import *


def main():
    while front_is_clear():
        build_tower()


def build_tower():
    while front_is_clear():
        put_beeper()
        move()
        put_beeper()
        column_return()


def column_return():
    while front_is_blocked():
        turn_around()
    while front_is_clear():
        move()
    next_tower()


def turn_around():
    for i in range(2):
        turn_left()


def next_tower():
    if right_is_clear():
        turn_right()
        move()
        turn_right()
    else:
        turn_around()
    while front_is_clear():
        move()


def turn_right():
    for i in range(3):
        turn_left()


if __name__ == "__main__":
    main()


#131


def filter_string_a(string):
    string.sort()
    filtered_string_list = []
    for stru in string:
        if stru.startswith("a"):
            filtered_string_list.append(stru)
    return filtered_string_list


input_string = ["apple", "banana", "avocado", "chewing", "apricot"]
output = filter_string_a(input_string)
print(output)


#132


def main():
    while front_is_clear():
        move()
    if front_is_blocked():
        turn_around()
        move()
        turn_left()
        move()
        pick_beeper()
        turn_left()
        turn_left()
    while front_is_clear():
        move()
    if front_is_blocked():
        turn_around()
        move()
        turn_around()


def turn_around():
    for i in range(3):
        left()


#133


def is_leap_year(year):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


def main():
    year = int(input("Enter a year: "))
    is_leap = is_leap_year(year)
    print(is_leap)


if __name__ == "__main__":
    main()


#134


def main():
    print("problem - 5")
    numb = int(input("write an integer number:"))
    mak_list = [int(x) for x in str(numb)]
    add_numb = 0
    for i in mak_list:
        add_numb += i
    print("Sum of the number's digits: ", add_numb)


if __name__ == "__main__":
    main()


#135


num = int(input("Enter a number: "))
Ans = 1
while num > 1:
    Ans *= num
    num -= 1
print(Ans)


#136


from karel.stanfordkarel import *

# This program makes Karel pick up
# a beeper and go back into her house.
def main():
    # Move to the beeper.
    move_beeper()
    # Pick the beeper up.
    pick_beeper()
    # Return to Karel's starting point.
    go_back()


# This function moves karel to the beeper.
def move_beeper():
    for i in range(2):
        move()
        turn_right()
        move()
        turn_left()
        move()


# this function return to Karel's starting point
def go_back():
    for i in range(2):
        turn_left()
        for i in range(3):
            move()
        turn_right()
        move()
        turn_right()


def turn_right():
    for i in range(3):
        turn_left()


if __name__ == "__main__":
    main()


#137


def main():
    my_word = input("Enter The original word: ")
    # Function calling
    reversed_word = reverse(my_word)
    print("The reversed word is: " + reversed_word)


# Helper Function
def reverse(word):
    # reversed - word
    new_word = ""
    # char by char
    for char in word:
        new_word = char + new_word
    # return
    return new_word


if __name__ == "__main__":
    main()


#138


input_number = int(input("Enter number"))
val = input_number
result = input_number
while val > 1:
    val = val - 1
    result = result * val
print("factorial of " + str(input_number) + " is " + str(result))


#139


def main():
    num = input("Input: ")
    sum = 0
    for n in num:
        sum += int(n)
    print(sum)


#140


def main():
    num = input("Enter the number you want to add: ")
    Sum = 0
    for i in str(num):
        Sum = Sum + int(i)
    print("Sum of the values you entered is", Sum)


#141


user_input = input("write your string here: ")
Upper = user_input.upper()
print(Upper)


#142


from karel.stanfordkarel import *

# Karel should fill the world with beepers.


def main():
    # decomposition using a function name for
    # each associated activity
    while left_is_clear():
        fill_one_row()
        return_to_row_start()
        move_up()
    # rewrite code after while loop to overcome
    # fencepost bug
    fill_one_row()


#143


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


if __name__ == "__main__":
    main()


#144


def main():
    vowel_count = 0
    vowels = ["a", "e", "i", "o", "u"]
    input_string = input("Enter the string:")
    input_string = input_string.lower()
    for char in input_string:
        for vowel in vowels:
            if char == vowel:
                vowel_count += 1
    print(vowel_count)


if __name__ == "__main__":
    main()


#145


def main():
    string = str(input("Enter string: "))
    for i in range((len(string) - 1), -1, -1):
        print(string[i])


#146


seq = [1, 2, 3, 4, 5, 6, 7, 8, 9]
seq_even = []
# It checks every element in list (sequence) - --
for i in seq:
    # it decides whether an element from sequence is even --.
    if i % 2 == 0:
        seq_even.append(i)  # appends even ; in empty list (seq_even)
print(seq_even)


#147


from graphics import Canvas

CANVAS_WIDTH = 300
CANVAS_HEIGHT = 300
CIRCLE_SIZE = 20
DELAY = 0.01


def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    while True:
        MOUSE_X = canvas.get_mouse_x()
        MOUSE_Y = canvas.get_mouse_y()
        if (
            MOUSE_X >= 0
            and MOUSE_X <= CANVAS_WIDTH
            and MOUSE_Y >= 0
            and MOUSE_Y <= CANVAS_HEIGHT
        ):
            pass


#148


# 1 karel Problem - Karel home
from karel.stanfordkarel import *

# This program defines a main function which should make karel
# move to the beeper, pick it up and return home
def main():
    get_out()
    pick_food()
    get_back_home()


# pre: Karel facing east, at the corner of starting position
# post: karel facing east, outside the home, at the position of beeper
def get_out():
    turn_right()
    move()
    turn_left()
    move()
    move()
    move()


# post: Karel facing west, at the position of beeper
def pick_food():
    pick_beeper()
    turn_around()


# post: Karel facing east, at the corner of starting position
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


if __name__ == "__main__":
    main()


#149


def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


print(factorial(5))


#150


def main():
    list1 = [1, 2, 3, 4]
    list2 = [3, 4, 5, 6]
    List = []
    for elem1 in list1:
        for elem2 in list2:
            if elem1 == elem2:
                elem = elem2
                List.append(elem)
    print(List)

    return


#151


String = input()
print(String[::-1])


#152


from karel.stanfordkarel import *


def main():
    turn_left()
    tower_N()
    tower_SC()
    move_4x()
    turn_left()
    tower_N()
    tower_SC()
    del tower_s()
    turn_3x()
    Tower()
    turn_left()
    del tower_NC()
    Tower()
    turn_3x()
    move_4x()
    del tower()


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


if __name__ == "__main__":
    main()


#153


def main():
    string = str(input("Enter string: "))
    for i in range((len(string) - 1), -1, -1):
        print(string[i])


if __name__ == "__main__":
    main()


#154


def main():
    num = int(input("Enter a num:"))
    if is_prime(num):
        print(f"Num is prime")
    else:
        print("Not prime")


def is_prime(n):
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    for i in range(5, int(n**0.5) + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True


if __name__ == "__main__":
    main()


#155


from karel.stanfordkarel import *


def main():
    turn_left()
    while front_is_clear():
        turn_right()
        fill_row()
        return_to_home()
        jump_row()
        turn_right()
        fill_row()
        return_to_home()
    while front_is_clear():
        move()

    def fill_row():
        while front_is_clear():
            put_beeper()
            move()
            put_beeper()


#156


from stanfordkarel import *

# Karel should fill the whole world with beepers.


def main():
    # You should write your code to make Karel do its task in this function.
    # Make sure to delete the 'pass' line before starting to write your own
    # code. You should also delete this comment and replace it with a
    # better, more descriptive one.

    while not left_is_blocked():
        put_beeper_line()
        reset_position()
        put_beeper_line()


def put_beeper_line():
    put_beeper()
    while front_is_clear():
        move()
        put_beeper()


#157


# Karel needs to move to the bottom of the next notch to come
# Hence building the next column.
# Precondition: Karel is facing east
# post-condition: Karel is facing east at the next column site.
def move_to_next_notch_bottom():
    if front_is_clear():
        for i in range(4):
            move()


def turn_around():
    turn_left()
    turn_left()


if __name__ == "__main__":
    main()


#158


def find_largest_smallest(numbers):
    if not numbers:
        return None
    smallest = largest = numbers[0]
    for num in numbers:
        if num < smallest:
            smallest = num
        if num > largest:
            largest = num
    return smallest, largest


# Example usage:
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
result = find_largest_smallest(numbers)
print(result)


#159


def main():
    user_number = input("Enter the number:\n")
    result = sum_of_digits(user_number)
    print("The sum of the digits is ", result)


def sum_of_digits(user_number):
    number_str = str(user_number)
    digit_sum = 0
    for digit in number_str:
        digit_sum += int(digit)
    return digit_sum


if __name__ == "__main__":
    main()


#160


def is_prime(n):
    """
    Returns True if n is prime, False otherwise
    """
    if n <= 1:
        return False
    for i in range(2, int(n * 0.5) + 1):
        if n % i == 0:
            return False
    return True


def main():
    """
    The main function.
    """
    n = int(input("Enter a number: "))
    if is_prime(n):
        print(n, "is a prime number.")
    else:
        print(n, "is not a prime number.")


if __name__ == "__main__":
    main()


#161


# Reverse String
def main():
    str = input("Input a string: ")
    rev_str = ""
    for i in str:
        rev_str = i + rev_str
    print(rev_str)


if __name__ == "__main__":
    main()


#162


# Write a Python program to find the longest word in a given text
def main():
    sentence = input("Input a sentence: ")
    lst = sentence.split()
    l_word = ""
    for word in lst:
        if len(word) > len(l_word):
            l_word = word
    print(l_word)


if __name__ == "__main__":
    main()


#163


def greatest_common_divisor(a, b):
    smaller_number = a if a < b else b
    common_divisor = []
    for i in range(1, smaller_number + 1):
        if a % i == 0 and b % i == 0:
            common_divisor.append(i)
    return common_divisor[-1]


#164


def main():
    # The program should determine whether the given year is a leap year
    # (divisible by 4, divisible by 100 but also by 400).
    print("This program will help you identify if a given year is a leap year or not.")
    print(" ")
    identify_a_leap_year()
    ask_for_a_new_year_to_identify()


def identify_a_leap_year():
    print("Please input a year below (in number form).")
    Year = int(input("Year: "))
    print(" ")
    if (Year % 4 == 0) or (Year % 100 == 0) or (Year % 400 == 0):
        print("The Year " + str(Year) + " " + "is a leap year.")
    else:
        print("The Year " + str(Year) + " " + "is not a leap year.")


def ask_for_a_new_year_to_identify():
    while True:
        print(" ")
        ask = input("Do you want to identify a new year? Yes/No: ")
        print(" ")
        if ask == "Yes" or ask == "yes":
            identify_a_leap_year()
        elif ask == "No" or ask == "no":
            print("Thank you. See you again!")
            break
        elif ask != "Yes" and ask != "yes" and ask != "No" and ask != "no":
            print("Wrong keyword. Please type the exact keyword.")


if __name__ == "__main__":
    main()


#165


Sum = 0
number = input()
for i in number:
    Sum += int(i)
print(Sum)


#166


def factorial(n):
    if n <= 1:
        return 1
    else:
        return factorial(n - 1) * n


print(factorial(int(input())))


#167


year = int(input())
if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
    print(True)
else:
    print(False)


#168


word = input()
word = "".join([i for i in word])
print(word)


#169


list1 = [1, 2, 3, 4]
list2 = [3, 4, 5, 6]
list3 = [i for i in list1 if i in list2]
print(list3)


#170


list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
even = [i for i in list1 if i % 2 == 0]
print(even)


#171


def main():
    year = int(input())
    if year % 4 == 0 and year % 100 != 0:
        print("True")
    elif year % 100 == 0 and year % 400 == 0:
        print("True")
    else:
        print("False")


if __name__ == "__main__":
    main()


#172


from karel.stanfordkarel import *


def main():
    build_column()
    step_up()
    build_column()
    step_up()
    build_column()
    step_up()
    build_column()


def build_column():
    turn_left()
    build_beeper()
    build_beeper()
    build_beeper()
    build_beeper()
    put_beeper()
    go_back()
    turn_left()


def build_beeper():
    put_beeper()
    move()


def go_back():
    turn_around()
    step_up()


def turn_around():
    turn_left()
    turn_left()


def step_up():
    move()
    move()
    move()
    move()


if __name__ == "__main__":
    main()


#173


def main():
    input_string = input("Input string:")
    ret = " "
    for ch in input_string:
        ret = ret + ch.upper()
    print(ret)


if __name__ == "__main__":
    main()


#174


from Karel.StanfordKarel import *


def main():
    move_to_beeper()
    pick_beeper()
    turn_around()
    return_to_start()


def move_to_beeper():
    while front_is_clear():
        move()
    turn_right()
    move()
    turn_left()
    move()


def turn_around():
    turn_left()
    turn_left()


#175


from karel.stanfordkarel import *


def main():
    while front_is_clear():
        fill_tower()


def fill_tower():
    while front_is_clear():
        put_beeper()
        move()
        put_beeper()
    column_return()


def column_return():
    while front_is_blocked():
        turn_around()
    while front_is_clear():
        move()
    next_tower()


def turn_around():
    for i in range(2):
        turn_left()


def next_tower():
    if right_is_clear():
        turn_right()
        move()
        turn_right()
    else:
        turn_around()
    while front_is_clear():
        move()


def turn_right():
    for i in range(3):
        turn_left()


if __name__ == "__main__":
    main()


#176


def filter_string_a(string):
    string.sort()
    filtered_string_list = []
    for stru in string:
        if stru.startswith("a"):
            filtered_string_list.append(stru)
    return filtered_string_list


input_string = ["apple", "banana", "avocado", "cherry", "apricot"]
output = filter_string_a(input_string)
print(output)


#177


def main():
    while front_is_clear():
        move()
    if front_is_blocked():
        turn_around()
        move()
        turn_left()
        move()
        pick_beeper()
        turn_left()
        turn_left()
    while front_is_clear():
        move()
    if front_is_blocked():
        turn_around()
        move()
        turn_around()


def turn_around():
    for i in range(3):
        left()


#178


def is_leap_year(year):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


def main():
    year = int(input("Enter a year: "))
    is_leap = is_leap_year(year)
    print(is_leap)


if __name__ == "__main__":
    main()


#179


def main():
    print("Problem - 5")
    numb = int(input("Write an integer number: "))
    mak_list = [int(x) for x in str(numb)]
    add_numb = 0
    for i in mak_list:
        add_numb += i
    print("Sum of the numbers: ", add_numb)


if __name__ == "__main__":
    main()


#180


num = int(input("Enter a number: "))
Ans = 1
while num > 1:
    Ans *= num
    num -= 1
print(Ans)


#181


from karel.stanfordkarel import *

# This program makes Karel pick up
# a beeper and go back into her house.
def main():
    # Move to the beeper.
    move_beeper()
    # Pick the beeper up.
    pick_beeper()
    # Return to Karel's starting point.
    go_back()
    # This function moves karel to the beeper.


def move_beeper():
    for i in range(2):
        move()
        turn_right()
        move()
        turn_left()
        move()
    # this function return to Karel's starting point


def go_back():
    for i in range(2):
        turn_left()
        for i in range(3):
            move()
        turn_right()
        move()
        turn_right()


def turn_right():
    for i in range(3):
        turn_left()


if __name__ == "__main__":
    main()


#182


def main():
    my_word = input("Enter The original word: ")
    # Function calling
    reversed_word = reverse(my_word)
    print("The reversed word is: " + reversed_word)


# Helper Function
def reverse(word):
    # reversed word
    new_word = ""
    # char by char
    for char in word:
        new_word = char + new_word
    # return
    return new_word


if __name__ == "__main__":
    main()


#183


input_number = int(input("Enter number"))
val = input_number
result = input_number
while val > 1:
    val = val - 1
    result = result & val
print("factorial f&" + str(input_number) + str(result))


#184


def main():
    num = input("Input : ")
    sum = 0
    for n in num:
        sum += int(n)
    print(sum)


#185


def main():
    num = input("enter the number you want to add: ")
    Sum = 0
    for i in str(num):
        Sum = Sum + int(i)
    print("Sum of the value you entered is", Sum)
    return


#186


user_input = input("write your string here:")
Upper = user_input.upper()
print(Upper)


#187


.python
from karel.stanfordkarel import *

# Karel should fill the world with beepers.

def main():
    # decomposition using a function name for
    # each associated activity
    while left_is_clear():
        fill_one_row()
        return_to_row_start()
        move_up()
    # rewrite code after while loop to overcome
    # fencepost bug
    fill_one_row()


#188


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


if __name__ == "__main__":
    main()


#189


def main():
    vowel_count = 0
    vowels = ["a", "e", "i", "o", "u"]
    input_string = input("Enter the string:")
    input_string = input_string.lower()
    for char in input_string:
        for vowel in vowels:
            if char == vowel:
                vowel_count += 1
    print(vowel_count)


if __name__ == "__main__":
    main()


#190


def main():
    string = str(input("Enter string: "))
    for i in range((len(string) - 1), -1, -1):
        print(string[i])


#191


seq = [1, 2, 3, 4, 5, 6, 7, 8, 9]
seq_even = []
# It checks every element in list (sequence)
for i in seq:
    # it decides whether an element from sequence is even
    if i % 2 == 0:
        seq_even.append(i)  # appends even ; in empty list (seq-even)
print(seq_even)


#192


from graphics import Canvas

CANVAS_WIDTH = 300
CANVAS_HEIGHT = 300
CIRCLE_SIZE = 20
DELAY = 0.01


def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    while True:
        MOUSE_X = canvas.get_mouse_x()
        MOUSE_Y = canvas.get_mouse_y()
        if (
            MOUSE_X >= 0
            and MOUSE_X <= CANVAS_WIDTH
            and MOUSE_Y >= 0
            and MOUSE_Y <= CANVAS_HEIGHT
        ):
            continue


#193


# 1 karel Problem - Karel home
from Karel.Stanfordkarel import *

# This program defines a main function which should make karel
# move to the beeper, pick it up and return home
def main():
    get_out()
    pick_food()
    get_back_home()


# pre: Karel facing east, at the corner of starting position
# post: Karel facing east, outside the home, at the position of beeper
def get_out():
    turn_right()
    move()
    turn_left()
    move()
    move()
    move()


# post: Karel facing west, at the position of beeper
def pick_food():
    pick_beeper()
    turn_around()


# post: Karel facing east, at the corner of starting position
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


if __name__ == "__main__":
    main()


#194


def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


print(factorial(5))


#195


def main():
    list1 = [1, 2, 3, 4]
    list2 = [3, 4, 5, 6]
    List = []
    for elem1 in list1:
        for elem2 in list2:
            if elem1 == elem2:
                elem = elem2
                List.append(elem)
    print(List)


main()


#196


String = input()
print(String[::-1])


#197


from Karel.Stanford import Kad


def main():
    turn_left()
    tower_N()
    tower_SC()
    move_4x()
    turn_left()
    tower_N()
    tower_SC()
    del tower_s()
    turn_3x()
    Tower()
    turn_left()
    del tower_NC()
    Tower()
    turn_3x()
    move_4x()
    del tower()
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

    if __name__ == "__main__":
        main()


#198


def main():
    string = str(input("Enter string: "))
    for i in range((len(string) - 1), -1, -1):
        print(string[i])


if __name__ == "__main__":
    main()


#199


def main():
    num = int(input("Enter a num: "))
    if is_prime(num):
        print(f"Num is prime")
    else:
        print("Num is not prime")


def is_prime(n):
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    for i in range(5, int(n**0.5) + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True


if __name__ == "__main__":
    main()


#200


from karel.stanfordkarel import *


def main():
    turn_left()
    while front_is_clear():
        turn_right()
        fill_row()
        return_to_home()
        jumprow()
        turn_right()
        fill_row()
        return_to_home()
    while front_is_clear():
        move()

    def fill_row():
        while front_is_clear():
            put_beeper()
            move()
        put_beeper()


#201


from stanfordkarel import *

# Karel should fill the whole world with beepers.


def main():
    # You should write your code to make Karel do its task in this function.
    # Make sure to delete the 'pass' line before starting to write your own code.

    while not left_is_blocked():
        put_beeper_line()
        reset_position()
        put_beeper_line()


def put_beeper_line():
    put_beeper()
    while front_is_clear():
        move()
        put_beeper()


#202


# Karel needs to move to the bottom of the next notch to come
# Hence building the next column.
# Precondition: Karel is facing east
# post-condition: Karel is facing east at the next column site.
def move_to_next_arch_bottom():
    if front_is_clear():
        for i in range(4):
            move()


def turn_around():
    turn_left()
    turn_left()


if __name__ == "__main__":
    main()


#203


def find_largest_smallest(numbers):
    if not numbers:
        return None
    smallest = largest = numbers[0]
    for num in numbers:
        if num < smallest:
            smallest = num
        if num > largest:
            largest = num
    return smallest, largest


# Example usage:
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
result = find_largest_smallest(numbers)
print(result)


#204


def main():
    user_number = input("Enter the number:\n")
    result = sum_of_digits(user_number)
    print("The sum of the digits is ", result)


def sum_of_digits(user_number):
    number_str = str(user_number)
    digit_sum = 0
    for digit in number_str:
        digit_sum += int(digit)
    return digit_sum


if __name__ == "__main__":
    main()


#205


def is_prime(n):
    """
    Returns True if n is prime, False otherwise
    """
    if n <= 1:
        return False
    for i in range(2, int(n * 0.5) + 1):
        if n % i == 0:
            return False
    return True


def main():
    """
    The main function.
    """
    n = int(input("Enter a number: "))
    if is_prime(n):
        print(n, "is a prime number.")
    else:
        print(n, "is not a prime number.")


if __name__ == "__main__":
    main()


#206


# Reverse String
def main():
    str = input("Input a string: ")
    rev_str = ""
    for i in str:
        rev_str = i + rev_str
    print(rev_str)


if __name__ == "__main__":
    main()


#207


# Write a Python program to find the longest word in a given text
def main():
    sentence = input("Input a sentence: ")
    word_list = sentence.split()
    l_word = ""
    for word in word_list:
        if len(word) > len(l_word):
            l_word = word
    print(l_word)


if __name__ == "__main__":
    main()


#208


def greatest_common_divisor(a, b):
    smaller_number = a if a < b else b
    common_divisor = []
    for i in range(1, smaller_number + 1):
        if a % i == 0 and b % i == 0:
            common_divisor.append(i)
    return common_divisor[-1]


#209


def main():
    # The program should determine whether the given year is a leap year
    # (divisible by 4, divisible by 100 but also by 400).
    print("This program will help you identify if a given year is a leap year or not.")
    print(" ")
    identify_a_leap_year()
    ask_for_a_new_year_to_identify()


def identify_a_leap_year():
    print("Please input a year below (in number form).")
    Year = int(input("Year: "))
    print(" ")
    if (Year % 4 == 0) and (Year % 100 != 0 or Year % 400 == 0):
        print("The Year " + str(Year) + " is a leap year.")
    else:
        print("The Year " + str(Year) + " is not a leap year.")


def ask_for_a_new_year_to_identify():
    while True:
        print(" ")
        ask = input("Do you want to identify a new year? Yes/No: ")
        print(" ")
        if ask == "Yes" or ask == "yes":
            identify_a_leap_year()
        elif ask == "No" or ask == "no":
            print("Thank you. See you again!")
            break
        else:
            print("Wrong keyword. Please type the exact keyword.")


if __name__ == "__main__":
    main()


#210


Sum = 0
number = input()
for i in number:
    Sum += int(i)
print(Sum)


#211


def factorial(n):
    if n <= 1:
        return 1
    else:
        return factorial(n - 1) * n


print(factorial(int(input())))


#212


year = int(input())
if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
    print(True)
else:
    print(False)


#213


word = input()
word = "".join([i for i in word])
print(word)


#214


list1 = [1, 2, 3, 4]
list2 = [3, 4, 5, 6]
list3 = [i for i in list1 if i in list2]
print(list3)


#215


list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
even = [i for i in list1 if i % 2 == 0]
print(even)


#216


def main():
    year = int(input())
    if year % 4 == 0 and year % 100 != 0:
        print("True")
    elif year % 100 == 0 and year % 400 == 0:
        print("True")
    else:
        print("False")


if __name__ == "__main__":
    main()


#217


from karel.stanfordkarel import *


def main():
    build_column()
    step_up()
    build_column()
    step_up()
    build_column()
    step_up()
    build_column()


def build_column():
    turn_left()
    build_beeper()
    build_beeper()
    build_beeper()
    build_beeper()
    put_beeper()
    go_back()
    turn_left()


def build_beeper():
    put_beeper()
    move()


def go_back():
    turn_around()
    step_up()


def turn_around():
    turn_left()
    turn_left()


def step_up():
    move()
    move()
    move()
    move()


if __name__ == "__main__":
    main()


#218


def main():
    input_string = input("Input string:")
    ret = " "
    for ch in input_string:
        ret = ret + ch.upper()
    print(ret)


if __name__ == "__main__":
    main()


#219


from Karel.StanfordKarel import *


def main():
    move_to_beeper()
    pick_beeper()
    turn_around()
    return_to_start()


def move_to_beeper():
    while front_is_clear():
        move()
    turn_right()
    move()
    turn_left()
    move()


def turn_around():
    turn_left()
    turn_left()


#220


from karel.stanfordkarel import *


def main():
    while front_is_clear():
        build_tower()


def build_tower():
    while front_is_clear():
        put_beeper()
        move()
        put_beeper()
        column_return()


def column_return():
    while front_is_blocked():
        turn_around()
    while front_is_clear():
        move()
    next_tower()


def turn_around():
    for i in range(2):
        turn_left()


def next_tower():
    if right_is_clear():
        turn_right()
        move()
        turn_right()
    else:
        turn_around()
    while front_is_clear():
        move()


def turn_right():
    for i in range(3):
        turn_left()


if __name__ == "__main__":
    main()


#221


def filter_string_a(string):
    string.sort()
    filtered_string_list = []
    for stru in string:
        if stru.startswith("a"):
            filtered_string_list.append(stru)
    return filtered_string_list


input_string = ["apple", "banana", "avocado", "chewing", "apricot"]
output = filter_string_a(input_string)
print(output)


#222


def main():
    while front_is_clear():
        move()
    if front_is_blocked():
        turn_around()
        move()
        turn_left()
        move()
        pick_beeper()
        turn_left()
        turn_left()
    while front_is_clear():
        move()
    if front_is_blocked():
        turn_around()
        move()
        turn_around()


def turn_around():
    for i in range(3):
        left()


#223


def is_leap_year(year):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


def main():
    year = int(input("Enter a year: "))
    is_leap = is_leap_year(year)
    print(is_leap)


if __name__ == "__main__":
    main()


#224


def main():
    print("problem - 5 ")
    numb = int(input("write an integer number:"))
    mak_list = [int(x) for x in str(numb)]
    add_numb = 0
    for i in mak_list:
        add_numb += i
    print("Sum of the number's digits: ", add_numb)


if __name__ == "__main__":
    main()


#225


num = int(input("Enter a number: "))
Ans = 1
while num > 1:
    Ans *= num
    num -= 1
print(Ans)


#226


from karel.stanfordkarel import *

# This program makes Karel pick up
# a beeper and go back into her house.
def main():
    # Move to the beeper.
    move_beeper()
    # Pick the beeper up.
    pick_beeper()
    # Return to Karel's starting point.
    go_back()


# This function moves karel to the beeper.
def move_beeper():
    for i in range(2):
        move()
        turn_right()
        move()
        turn_left()
        move()


# this function return to Karel's starting point
def go_back():
    for i in range(2):
        turn_left()
    for i in range(3):
        move()
        turn_right()
        move()
    turn_right()


def turn_right():
    for i in range(3):
        turn_left()


if __name__ == "__main__":
    main()


#227


def main():
    my_word = input("Enter The original word: ")
    # Function calling
    def reverse(word):
        new_word = ""
        # reversed - word
        for char in word:
            new_word = char + new_word
        return new_word

    reversed_word = reverse(my_word)
    print("The reversed word is: " + reversed_word)


if __name__ == "__main__":
    main()


#228


input_number = int(input("Enter number"))
val = input_number
result = input_number
while val > 1:
    val = val - 1
    result = result * val
print("factorial of " + str(input_number) + " is " + str(result))


#229


def main():
    num = input("Input: ")
    sum = 0
    for n in num:
        sum += int(n)
    print(sum)


#230


def main():
    num = input("Enter the number you want to add: ")
    Sum = 0
    for i in str(num):
        Sum = Sum + int(i)
    print("Sum of the values you entered is", Sum)


main()


#231


user_input = input("write your string here: ")
upper = user_input.upper()
print(upper)


#232


from karel.stanfordkarel import *

# Karel should fill the world with beepers.


def main():
    # Decomposition using a function name for
    # each associated activity
    while left_is_clear():
        fill_one_row()
        return_to_row_start()
        move_up()
    # Rewrite code after while loop to overcome
    # fencepost bug
    fill_one_row()


#233


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


if __name__ == "__main__":
    main()


#234


def main():
    vowel_count = 0
    vowels = ["a", "e", "i", "o", "u"]
    input_string = input("Enter the string:")
    input_string = input_string.lower()
    for char in input_string:
        for vowel in vowels:
            if char == vowel:
                vowel_count += 1
    print(vowel_count)


if __name__ == "__main__":
    main()


#235


def main():
    string = str(input("Enter string: "))
    for i in range((len(string) - 1), -1, -1):
        print(string[i])


#236


seq = [1, 2, 3, 4, 5, 6, 7, 8, 9]
seq_even = []

# It checks every element in list (sequence)
for i in seq:
    # it decides whether an element from sequence is even
    if i % 2 == 0:
        seq_even.append(i)  # appends even numbers in empty list (seq_even)
print(seq_even)


#237


from graphics import Canvas

canvas_width = 300
canvas_height = 300
circle_size = 20
delay = 0.01


def main():
    canvas = Canvas(canvas_width, canvas_height)
    while True:
        mouse_x = canvas.get_mouse_x()
        mouse_y = canvas.get_mouse_y()
        if (
            mouse_x >= 0
            and mouse_x <= canvas_width
            and mouse_y >= 0
            and mouse_y <= canvas_height
        ):
            continue


#238


# 1 karel Problem - Karel home
from Karel.Stanfordkarel import *

# This program defines a main function which should make karel
# move to the beeper, pick it up and return home
def main():
    get_out()
    pick_food()
    get_back_home()


# pre: Karel facing east, at the corner of starting position
# post: karel facing east, outside the home, at the position of beeper
def get_out():
    turn_right()
    move()
    turn_left()
    move()
    move()
    move()


# post: Karel facing west, at the position of beeper
def pick_food():
    pick_beeper()
    turn_around()


# post: Karel facing east, at the corner of starting position
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


if __name__ == "__main__":
    main()


#239


def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


print(factorial(5))


#240


_plus


def main():
    list1 = [1, 2, 3, 4]
    list2 = [3, 4, 5, 6]
    List = []
    for elem1 in list1:
        for elem2 in list2:
            if elem1 == elem2:
                List.append(elem2)
    print(List)

    return


#241


String = input()
print(String[::-1])


#242


from karel.stanfordkarel import *


def main():
    turn_left()
    tower_N()
    tower_SC()
    move_4x()
    turn_left()
    tower_N()
    tower_SC()
    del tower_s()
    turn_3x()
    Tower()
    turn_left()
    del tower_NC()
    Tower()
    turn_3x()
    move_4x()
    del tower()


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


if __name__ == "__main__":
    main()


#243


def main():
    string = str(input("Enter string: "))
    for i in range(len(string) - 1, -1, -1):
        print(string[i])


if __name__ == "__main__":
    main()


#244


def main():
    num = int(input("Enter a num: "))
    if is_prime(num):
        print(f"num is prime")
    else:
        print("num not prime")


def is_prime(n):
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    for i in range(5, int(n**0.5) + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True


if __name__ == "__main__":
    main()


#245


from karel.stanfordkarel import *


def main():
    turn_left()
    while front_is_clear():
        turn_right()
        fill_row()
        return_to_home()
        jump_row()
        turn_right()
        fill_row()
        return_to_home()
    while front_is_clear():
        move()

    def fill_row():
        while front_is_clear():
            put_beeper()
            move()
        put_beeper()


#246


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


#247


# Karel needs to move to the bottom of the next arch to come
# Hence building the next column.
# Precondition: Karel is facing east
# post-condition: Karel is facing east at the next column site.
def move_to_next_arch_bottom():
    if front_is_clear():
        for i in range(4):
            move()


def turn_around():
    turn_left()
    turn_left()


if __name__ == "__main__":
    main()


#248


def find_largest_smallest(numbers):
    if not numbers:
        return None
    smallest = largest = numbers[0]
    for num in numbers:
        if num < smallest:
            smallest = num
        if num > largest:
            largest = num
    return smallest, largest


# Example usage:
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
result = find_largest_smallest(numbers)
print(result)


#249


def main():
    user_number = input("Enter the number:\n")
    result = sum_of_digits(user_number)
    print("The sum of the digits is ", result)


def sum_of_digits(user_number):
    number_str = str(user_number)
    digit_sum = 0  # zero
    for digit in number_str:
        digit_sum += int(digit)
    return digit_sum


if __name__ == "__main__":
    main()


#250


def is_prime(n):
    """
    Returns True if n is prime, False otherwise
    """
    if n <= 1:
        return False
    for i in range(2, int(n * 0.5) + 1):
        if n % i == 0:
            return False
    return True


def main():
    """
    The main function.
    """
    n = int(input("Enter a number: "))
    if is_prime(n):
        print(n, "is a prime number.")
    else:
        print(n, "is not a prime number.")


if __name__ == "__main__":
    main()


#251


# Reverse String
def main():
    str = input("Input a string: ")
    r_str = ""
    for i in str:
        r_str = i + r_str
    print(r_str)


if __name__ == "__main__":
    main()


#252


# Write a Python program to find the longest word in a given text
def main():
    sentence = input("Input a sentence: ")
    list = sentence.split()
    Lword = ""
    for word in list:
        if len(word) > len(Lword):
            Lword = word
    print(Lword)


if __name__ == "__main__":
    main()


#253


def greatest_common_divisor(a, b):
    smaller_number = a if a < b else b
    common_divisor = []
    for i in range(1, smaller_number + 1):
        if a % i == 0 and b % i == 0:
            common_divisor.append(i)
    return common_divisor[-1]


#254


def main():
    # The program should determine whether the given year is a leap year
    # (divisible by 4, divisible by 100 but also by 400).
    print("This program will help you identify if a given year is a leap year or not.")
    print("")
    identify_a_leap_year()
    ask_for_a_new_year_to_identify()


def identify_a_leap_year():
    print("Please input a year below (in number form).")
    Year = int(input("Year:"))
    print("")
    if (Year % 4 == 0) and ((Year % 100 != 0) or (Year % 400 == 0)):
        print("The Year " + str(Year) + " " + "is a leap year.")
    else:
        print("The Year " + str(Year) + " " + "is not a leap year.")


def ask_for_a_new_year_to_identify():
    while True:
        print("")
        ask = input("Do you want to identify a new year? Yes/No: ")
        print("")
        if ask == "Yes" or ask == "yes":
            identify_a_leap_year()
        elif ask == "No" or ask == "no":
            print("Thank you. See you again!")
            break
        elif ask != "Yes" and ask != "yes" and ask != "No" and ask != "no":
            print("Wrong keyword. Please type the exact keyword.")


if __name__ == "__main__":
    main()


#255


Sum = 0
number = input()
for i in number:
    Sum += int(i)
print(Sum)


#256


def factorial(n):
    if n <= 1:
        return 1
    else:
        return factorial(n - 1) * n


print(factorial(int(input())))


#257


year = int(input())
if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
    print(True)
else:
    print(False)


#258


word = input()
word = "".join([i for i in word[::-1]])
print(word)


#259


list1 = [1, 2, 3, 4]
list2 = [3, 4, 5, 6]
list3 = [i for i in list1 if i in list2]
print(list3)


#260


list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
even = [i for i in list1 if i % 2 == 0]
print(even)


#261


def main():
    year = int(input())
    if year % 4 == 0 and year % 100 != 0:
        print("True")
    elif year % 100 == 0 and year % 400 == 0:
        print("True")
    else:
        print("False")


if __name__ == "__main__":
    main()


#262


from karel.stanfordkarel import *


def main():
    build_column()
    step_up()
    build_column()
    step_up()
    build_column()
    step_up()
    build_column()


def build_column():
    turn_left()
    build_beeper()
    build_beeper()
    build_beeper()
    build_beeper()
    put_beeper()
    go_back()
    turn_left()


def build_beeper():
    put_beeper()
    move()


def go_back():
    turn_around()
    step_up()


def turn_around():
    turn_left()
    turn_left()


def step_up():
    move()
    move()
    move()
    move()


if __name__ == "__main__":
    main()


#263


def main():
    input_string = input("Input string:")
    ret = " "
    for ch in input_string:
        ret = ret + ch.upper()
    print(ret)


if __name__ == "__main__":
    main()


#264


from Karel.StanfordKarel import *


def main():
    move_to_beeper()
    pick_beeper()
    turn_around()
    return_to_start()


def move_to_beeper():
    while front_is_clear():
        move
    turn_right()
    move()
    turn_left()
    move()


def turn_around():
    turn_left()
    turn_left()


#265


from karel.stanfordkarel import *


def main():
    while front_is_clear():
        build_tower()


def build_tower():
    while front_is_clear():
        put_beeper()
        move()
        put_beeper()
        column_return()


def column_return():
    while front_is_blocked():
        turn_around()
    while front_is_clear():
        move()
    next_tower()


def turn_around():
    for i in range(2):
        turn_left()


def next_tower():
    if right_is_clear():
        turn_right()
        move()
        turn_right()
    else:
        turn_around()
    while front_is_clear():
        move()


def turn_right():
    for i in range(3):
        turn_left()


if __name__ == "__main__":
    main()


#266


def filter_string_a(string):
    string.sort()
    filtered_string_list = []
    for stru in string:
        if stru.startswith("a"):
            filtered_string_list.append(stru)
    return filtered_string_list


input_string = ["apple", "banana", "avocado", "chewing", "apricot"]
output = filter_string_a(input_string)
print(output)


#267


def main():
    while front_is_clear():
        move()
    if front_is_blocked():
        turn_around()
        move()
        turn_left()
        move()
        pick_beeper()
        turn_left()
        turn_left()
    while front_is_clear():
        move()
    if front_is_blocked():
        turn_around()
        move()
        turn_around()


def turn_around():
    for i in range(3):
        left()


#268


def is_leap_year(year):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


def main():
    year = int(input("Enter a year: "))
    is_leap = is_leap_year(year)
    print(is_leap)


if __name__ == "__main__":
    main()


#269


def main():
    print("Problem - 5 ")
    num = int(input("Write an integer number: "))
    mak_list = [int(x) for x in str(num)]
    add_num = 0
    for i in mak_list:
        add_num += i
    print("Sum of the numbers: ", add_num)


if __name__ == "__main__":
    main()


