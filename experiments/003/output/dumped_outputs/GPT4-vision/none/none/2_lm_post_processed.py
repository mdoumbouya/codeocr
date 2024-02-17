def main():
    # input
    my_word = input("Enter the original word: ")
    # function calling
    reversed_word = reverse(my_word)
    print("The original word is "+ " " + "reversed_word")
# Helper Function

def reverse(word):
    # reversed word
    new_word = ''
    # sort by char
    for char in word:
        new_word = char + new_word
    # return new word
    return new_word

if __name__ == "__main__":
    main()
