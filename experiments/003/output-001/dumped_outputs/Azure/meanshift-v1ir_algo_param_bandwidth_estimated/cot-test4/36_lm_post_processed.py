def main ():
    year = int (input())
    if ( year % 4 == 0 and year % 100 != 0):
        print ("True")
    elif (year % 100 == 0 and year % 400 == 0):
        print ("True")
    else:
        print ("False")

if __name__ == "__main__":
    main ()
