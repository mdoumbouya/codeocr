def is_prime(n):
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
