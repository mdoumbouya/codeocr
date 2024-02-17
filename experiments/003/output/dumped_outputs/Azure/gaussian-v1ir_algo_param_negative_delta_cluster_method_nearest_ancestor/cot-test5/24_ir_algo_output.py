def main():
    user-number = input ("Enter the number: ")
    result = sum_of_digits (user_number)
    print ("The sum of the digits is ", result)
def Sum_of_digits (user_ number):
    number_str = Str (user_number)
    digit-sum=0 # zero
    for digit in number- str:
        digit_sum + = int (digit)
    return digit sum
if _name_ = "_main_":
    main ()
