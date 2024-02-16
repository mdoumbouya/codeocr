def main():
    # The program should determine whether the given year is a leap year
    # (divisible by 4, divisible by 100 but also by 400).
    print("This program will help you identify if a given year is a leap year or not.")
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
