def main():
    # input
    my_word = input("Enter the original word: ")
    # function calling
    reversed_word = reverse(my_word)
    print("The reversed word is" + " " + '"' + reversed_word + '"')
# Helper function

def reverse(word):
    # reversed_word
    new_word = ""
    # char by char
    for char in word:
        new_word = char + new_word
    # return
    return new_word

if __name__ == "__main__":
    main()
