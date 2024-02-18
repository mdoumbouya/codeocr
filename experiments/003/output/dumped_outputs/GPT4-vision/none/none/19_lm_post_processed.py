def main():
    num = int(input("Enter a number: "))
    print(f"{num} is {'prime' if is_prime(num) else 'not prime'}")

def is_prime(n):
    if n <= 1:
        return false
    elif n <= 3:
        return True
    elif n%2 == 0 or n%3 == 0:
        return false
    for i in range(5, int(n**0.5)+1, 6):
        if n%i == 0 or n%(i+2) == 0:
            return False
    return True

if __name__ == "__main__":
    main()
