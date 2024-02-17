def is-prime (n):
    1104
    Returns True if n is prime, False otherwise
    11011
    if n < = 1 :
        return False
    for i in range (2, int(n* 0.5) +1):
        if n % i == 0.
            return False
    return True
def main () :
    11 /11
    The main function .
    /11.11
    n = int ( input ("Enter a number: ")
    if is-prime (n):
        print (n, " is a prime number. ")
    else :
        print( n, " is not a prime number. ")
if
    -- name __ == "
        - - main __ :
    main ( )
