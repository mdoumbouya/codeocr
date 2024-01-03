def is_leap_year(year):
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
