def main():
    print(" problem - 5")
    print("--------------")
    print("write an integer number; ")
    numb = int(input())
    mak_list = [int(x) for x in str(numb)]
    add_numb = 0
    for i in mak_list:
        add_numb += i
    print("sum of the numbers: ", add_numb)

if __name__ == "__main__":
    main()
