def main():
user_number = input("Enter the number: ")
result = sum_of_digits(user_number)
print("The sum of the digits is ", result)

def sum_of_digits(user_number):
number_str = str(user_number)
digit_sum = 0 # zero
for digit in number_str:
    digit_sum += int(digit)
return digit_sum

if __name__ == "__main__":
main()
