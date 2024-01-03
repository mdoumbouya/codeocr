def main():
    my_word = input("Enter The original word: ")
    #Function calling
    reversed_word = reverse(my_word)
    print("The reversed word is: " + reversed_word)
# Helper Function

def reverse(word):
    # reversed word
    new_word = ""
    # char by char
    for char in word:
        new_word = char + new_word
    # return
    return new_word

if __name__ == "__main__":
    main()
