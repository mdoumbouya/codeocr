def main () :
    print ("problem - 5 ")
    print (") --")
    numb = int (input ('write an integer number:'))
    mak_list = [int (x) for x in str (numb)]
    add_numb = 0
    for i in mak_list :
        add_numb += i
    print ("Sum of the number's: ", add_numb)

if __name__ == "__main__":
    main()
