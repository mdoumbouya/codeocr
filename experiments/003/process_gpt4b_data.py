import json
import copy
import pandas as pd
import editdistance
from tqdm import tqdm

# This file is used to process manually collected gpt4b data.



image_id0_variant1 = '''num = int(input("Enter a number: "))
Ans = 1

while num > 1:
    Ans *= num
    num -= 1

return Ans
'''
image_id0_variant2 = '''num = int(input("Enter a number: "))

if num > 0:
    while num != 1:
        if num % 2 == 0:
            num = num // 2
        else:
            num = 3 * num + 1
    print("Ends at number: 1")
'''


gpt4b_outputs = {
    0 : image_id0_variant1,
    1 : '''from karel.stanfordkarel import *

#This program makes Karel pick up
#a beeper and go back into her house.
def main():
    #Move to the beeper.
    move_beeper()
    #Pick the beeper up.
    pick_beeper()
    #Return to Karel's starting point.
    go_back()

#This function moves Karel to the beeper.
def move_beeper():
    for j in range(2):
        move()
    turn_right()
    move()
    turn_left()
    move()

# this function return to Karel's starting point.
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
''',
  2 : '''def main():
    # input
    my_word = input('Enter the original word: ')

    # function calling
    reversed_word = reverse(my_word)
    print('The reversed word is: ' + reversed_word)

# Helper function
def reverse(word):
    # reversed_word
    new_word = ''

    # sort by char
    for char in word:
        new_word = char + new_word
    # return
    return new_word

if __name__ == '__main__':
    main()
''',
  3 : '''input_number = int(input('Enter number:'))

val = input_number
result = input_number

while (val > 1):
    val = val - 1
    result = result * val

print('factorial of ' + str(input_number) + ' is ' + str(result))
''',
  4 : '''def main():
    num = input('input :')
    sum = 0
    for h in num:
        sum += int(h)
    print(sum)
''',
  5 : '''def main():
    num = input('enter the number you want to add')
    Sum = 0
    for i in str(num):
        Sum = Sum + int(i)
    print('Sum of the value you entered is', Sum)
''',
  6 : '''user_input = input("Write your string here:")
upper = user_input.upper()
print(upper)
''',
  7 : '''from karel.stanfordkarel import *

"""
Karel should fill the world with beepers.
"""
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

''',
  8 : '''from karel.stanfordkarel import *

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
''',
  9 : '''def main():
    vowel_count = 0
    vowels = ['a', 'e', 'i', 'o', 'u']

    input_string = input("Enter the string: ")
    input_string = input_string.lower()

    for char in input_string:
        for vowel in vowels:
            if char == vowel:
                vowel_count += 1

    print(vowel_count)

if __name__ == '__main__':
    main()
''',
  10 : '''def main():
    string = str(input('Enter a string:'))
    for i in range(len(string)-1, -1, -1):
        print(string[i])
''',
  11 : '''seq = [1, 2, 3, 4, 5, 6, 7, 8, 9]

seq_even = []

# It checks every element in list(sequence)---
for i in seq:

    # it decides whether an element from sequence is even---
    if i % 2 == 0:
        seq_even.append(i) # appends even i in empty list (seq_even)

print(seq_even)
''',
  12 : '''from graphics import canvas

CANVAS_WIDTH = 300
CANVAS_HEIGHT = 300
CIRCLE_SIZE = 20

DELAY = 0,0,0

def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    while True:
        mouse_x = canvas.get_mouse_x()
        mouse_y = canvas.get_mouse_y()

        if mouse_x >= 0 and mouse_x < CANVAS_WIDTH and mouse_y >= 0 and mouse_y < CANVAS_HEIGHT:
''',
  13 : '''# 1 karel Problem - karel home

from karel.stanfordkarel import *

# This program defines a main function which should make karel 
# move to beeper, pick it up and return home.

def main():
    get_out()
    pick_food()
    get_back_home()

# pre: karel facing east, at the corner of starting position
# post: karel facing east, outside the home, at the position of beeper
def get_out():
    turn_right()
    move()
    turn_left()
    move()
    move()
    move()
    move()

# post: karel facing west, at the position of beeper
def pick_food():
    pick_beeper()

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
''',
  14 : '''def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

print(factorial(5))
''',
  15 : '''def main():
    lst1 = [1,2,3]
    lst2 = [3,4,5]
    lst = []
    for elem1 in lst1:
        for elem2 in lst2:
            if elem1 == elem2:
                elem = elem1 + elem2
                lst.append(elem)
    print(lst)
''',
  16 : '''String = input()
print(String[::-1])
''',
  17 : '''from karel.stanfordkarel import *

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
''',
  18 : '''def main():
    string = str(input('Enter string: '))
    for i in range(len(string)-1, -1, -1):
        print(string[i])

if __name__ == '__main__':
    main()
''',
  19 : '''def main():
    num = int(input("Enter a number: "))
    print("num is prime" if is_prime(num) else "not prime")

def is_prime(n):
    if n < 2:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    for i in range(5, int(n * 0.5) + 1):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True

if __name__ == "__main__":
    main()
''',
  20 : '''from karel.stanfordkarel import *

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
''',
  21 : '''from stanfordkarel import *

"""
Karel should fill the whole world with beepers.
"""

def main():
    """
    You should write your code to make Karel do its task in this function.
    Make sure to delete the pass line before starting to write your own code. You should also delete this comment and replace it with a better, more descriptive one.
    """
    while not left_is_blocked():
        put_beeper_line()
        reset_position()
        put_beeper_line()

def put_beeper_line():
    put_beeper()
    while front_is_clear():
        move()
        put_beeper()
''',
  22 : '''#karel needs to move to the bottom of the next arch to commenc.
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
''',
  23 : '''def find_lrgst_smallest(number):
    if not numbers:
        return None
    smallest = largest = number[0]
    for num in numbers:
        if num < smallest:
            smallest = num
        if num > largest:
            largest = num
    return smallest, largest

#Example usage:
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
result = find_lrgst_smallest(numbers)
print(result)
''',
  24 : '''def main():
    user_number = input("Enter the number: ")
    result = sum_of_digits(user_number)
    print("The sum of the digits is", result)

def sum_of_digits(user_number):
    number_str = str(user_number)
    digit_sum = 0  # zero

    for digit in number_str:
        digit_sum += int(digit)

    return digit_sum

if __name__ == "__main__":
    main()
''',
  25 : '''def is_prime(n):
    """
    Returns True if n is prime, False otherwise.
    """
    if n <= 1:
        return False
    for i in range(2, int(n**0.5)+1):
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
''',
  26 : '''#Reverse String
def main():
    str = input("Input a string: ")
    r_str = ""
    for i in str:
        r_str = i + r_str
    print(r_str)

if __name__ == "__main__":
    main()
''',
  27 : '''# Write a Python program to find the longest word in a given text
def main():
    sentence = input("Input a sentence: ")
    list = sentence.split()
    l_word = ''
    for word in list:
        if len(word) > len(l_word):
            l_word = word
    print(l_word)

if __name__ == "__main__":
    main()
''',
  28 : '''def greatest_common_divisor(a,b):
    smaller_number=a if a<b else b
    common_divisor=[]
    for i in range(1, smaller_number+1):
        if a%i==0 and b%i==0:
            common_divisor.append(i)
    return common_divisor[-1]
''',
  29 : '''def main():
    """
    The program should determine whether the given year is a leap year
    (divisible by 4, divisible by 100 but also by 400).
    """
    print("This program will help you identify if a given year is a leap year or not.")
    print(" ")
    identify_a_leap_year()
    ask_for_a_new_year_to_identify()

def identify_a_leap_year():
    print("Please input a year below (in number form):")
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
''',
  30 : '''sum = 0
number = input()
for i in number:
    sum += int(i)
print(sum)
''',
  31 : '''def factorial(n):
    if n <= 1:
        return 1
    else:
        return factorial(n-1) * n

print(factorial(int(input())))
''',
  32 : '''year = int(input())

if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
    print(True)
else:
    print(False)
''',
  33 : '''Word = input()

Word = ''.join(['i' for i in Word[::-1]])

print(Word)
''',
  34 : '''list1 = [1, 2, 3, 4]
list2 = [3, 4, 5, 6]

list3 = [i for i in list1 if i in list2]
print(list3)
''',
  35 : '''list1 = [1,2,3,4,5,6,7,8,9]

even = [i for i in list1 if i%2==0]

print(even)
''',
  36 : '''def main():
    year = int(input())
    if (year % 4 == 0 and year % 100 != 0):
        print("True")
    elif (year % 100 == 0 and year % 400 == 0):
        print("True")
    else:
        print("false")

if __name__ == "__main__":
    main()
''',
  37 : '''from karel.stanfordkarel import *

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

if __name__ == '__main__':
    main()
''',
  38 : '''def main():
    input_string = (input('Input string: '))
    ret = ""
    for ch in input_string:
        ret = ret + ch.upper()
    print ret

if __name__ == '__main__':
    main()
''',
  39 : '''from Karel.StanfordKarel import *

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
''',
  40 : '''from karel.stanfordkarel import *

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
        move()
        turn_right()
    else:
        turn_around()
        while front_is_clear():
            move()

def turn_right():
    for i in range(3):
        turn_left()

if __name__ == '__main__':
    main()
''',
  41 : '''def filter_string_a(string):
    string.sort()
    filtered_string_list = []
    for str in string:
        if str.startswith("a"):
            filtered_string_list.append(str)
    return filtered_string_list

input_string = ["apple", "banana", "avocado", "cherry", "apricot"]
output = filter_string_a(input_string)
print(output)
''',
  42 : '''def main():
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
        turn_left()
''',
  43 : '''def is_leap_year(year):
    if year % 4 == 0:
        if year % 100 = 0:
            if year % 400 == 0:
                return True
            elbe:
                return False
        elbe:
            return False
    else:
        return False

def main():
    yearc = int(input("Enter a year: "))
    is_leap = is_leap_year(yearc)
    print(is_leap)

if __name__ == "__ main__":
    main()
''',
  44 : '''def main():
    print(" problem - 5")
    print("--------------")
    print("write an integer number; ")
    numb = int(input())
    mak_list = [int(x) for x in str(numb)]

    add_numb = 0
    for i in mak_list:
        add_numb += i

    print("sum of the numbers: ", add_numb)

if __name__ == "__main__":
    main()
''',
  45 : '''list = [6, 14, 5, 8, 9]

for elem in list:
    max = 0
    if elem > max:
        max = elem

return max
''',
  46 : '''def palindromic(stro):

    for i in range(int(len(stro)/2)):
        if stro[i] != str[len(stro)-i]:
            return False

    return True
''',
  47 : '''def factorial(n):

    result = n * factorial(n-1)
    
    return result
''',
  48 : '''def fibonacci(n):
    sequence = [0,1]
    i = 0
    while len(sequence) <= n:
        sequence.append(sequence[i+1] + sequence[i+2])
        i += 1
    return sequence

result = fibonacci(6)
print(result)
''',
  49 : '''def CountFrequency(my_list):
    freq = {}
    for item in my_list:
        freq[item] += 1
    return freq
''',
  50 : '''def twoSum(nums, target):
    for i in range(len(nums)):
        for p in range(i, len(nums)):
            if(nums[i] + nums[p] == target):
                return (i, p)
''',
  51 : '''def removeDuplicate():
    for num in duplicate:
        final_list = []
        if num not in final_list:
            final_list.append(num)
    return final_list
''',
  52 : '''def even_or_odd(number):
    if number / 2 == 0:
        return "Even"
    if number / 2 != 0:
        return "Odd"
''',
  53 : '''def upper_lower_count(str):
    upper_case = 0
    lower_case = 0
    for char in str:
        if char.isupper():
            upper_case += 1
        else:
            lower_case += 1
    return upper_case, lower_case
''',
  54 : '''def multiply(numbers):
    total = 0
    for x in numbers:
        total *= x
    return total
''',
}

# Done - 1, 2, 20, 21, 27, 40, 41, 29, 45 - 54

from code_ocr.global_utils import *


with open('output/postprocessed_ocr_provider_data.json') as f:
    data = json.load(f)

with open('../rawdata.csv') as f:
    rd = pd.read_csv(f)
    
output = []


for datum in tqdm(data, desc='Iteration'):

    copied_datum = copy.deepcopy(datum)
    copied_datum['ocr_provider'] = 'none'
    copied_datum['ocr_ouptut'] = 'none'
    copied_datum['ir_algo_name'] = 'none'
    copied_datum['ir_algo_output_code'] = 'none'
    copied_datum['ir_algo_output_edit_distance'] = 0
    copied_datum['prompting_method'] = 'GPT-4b'
    # copied_datum['lm_post_processed_code'] = str(gpt4b_outputs[datum['image_id']])
    copied_datum['lm_post_processed_code'] = remove_blank_lines(str(gpt4b_outputs[datum['image_id']]))
    copied_datum['lm_post_processed_edit_distance'] = editdistance.eval(copied_datum['lm_post_processed_code'], rd['Ground Truth'][datum['image_id']])
    
    output.append(copied_datum)
    
    
with open('output/gpt4b_multimodal_manual.json', 'w') as f:
    json.dump(output, f)
    
    
    
