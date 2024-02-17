def main ( ) :
    The program should determine whether the given year is a leap year
    ( divisible by 4, divisible by 100 but also by 400).
    print ( " This program will help you identify if a given year is a leap
        year or not . ")
    print ( "
    identify_a_ leap year ()
    ask _ for _ a _ new _year _ to _identify ( )
def identify_ a_ leap-year () :
    print ("Please input a year below ( in number form). ")
    Year = int (input ("Year:
    print (" ")
    if (Year % 4 == 0) or (Year % 100 == 0) or (year % 400 == 0) ;
        print ("The Year" + str (Year) + " "+ " is a leap year. ")
    else :
        print ( " the Year " + str ( Year ) + " " + " is not a leap year . " )
def ask-for-a-new year_ to _ identify ( ) :
    while True :
        print (" ")
        ask - input ( " Do you want to identify a new year ? Yes / No : " )
        print (" ")
        if ask == "Yes " or ask == "yes":
            identify_ a _ leap - year ( )
        elif ask == "No" or ask = "no":
            print ( " Thank you . See you again ! ")
            break
        elif ask != "Yes or ask ! = "yes" a ask != "No" or ask != "no".
            print ( " Wrong keyword . Please type the exact keyword . ")
if
_ name_ == " __ main __ ":
    main ()
