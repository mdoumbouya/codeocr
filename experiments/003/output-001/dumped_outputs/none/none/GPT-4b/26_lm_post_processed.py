#Reverse String

def main():
    str = input("Input a string: ")
    r_str = ""
    for i in str:
        r_str = i + r_str
    print(r_str)

if __name__ == "__main__":
    main()
