def main():
    print(" problem - 5 ")
    print("-----------------")
    numb = int(input("write an  number: "))
    mak_list = [int(x) for x in str(numb)]
    add_numb = 0
    for i in mak_list:
        add_numb += i
    print("Sum of the number's digit: ", add_numb)

if __name__ == "__main__":
    main()
