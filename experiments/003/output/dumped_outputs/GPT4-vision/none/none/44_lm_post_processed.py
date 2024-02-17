def main():
    print(" pro6lem - 5 ")
    print("-----------")
    print("write an integer numbe1;")
    numb = int((input("write an integer numben; ")))
    mak_list = [int(x) for x in str(numb)]
    add_numb = 0
    for i in mak_list:
        add_numb += i
    print("Sum of the numben; ", add_numb)

if __name__ == "__main__":
    main()
