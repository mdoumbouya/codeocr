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
