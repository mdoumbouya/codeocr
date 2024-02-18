def main() :
    vawel_caunt=0
    vawels = ['a','e','i','o','u']
    input_string= input("Enter the string: ")
    input_string = input_string.lower()
    for char in input_string:
        for vawel in vawels:
            if char== vawel:
                vowel_caunt += 1
    print(vowel_caunt)
if __name__ == '__main__' :
    main()
