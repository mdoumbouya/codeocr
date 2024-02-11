# Write a Python program to find the longest word in a given text

def main():
    sentence = input("Input a sentence: ")
    List = sentence.split()
    L_word = ""
    for word in List:
        if len(word) > len(L_word):
            L_word = word
    print(L_word)
if __name__=="__main__":
    main()
