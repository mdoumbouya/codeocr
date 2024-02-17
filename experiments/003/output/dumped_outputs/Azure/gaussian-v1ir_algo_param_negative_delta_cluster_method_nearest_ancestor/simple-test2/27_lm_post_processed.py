# Write a Python program to find the longest word in a given text

def main():
    sentence = input("Input a sentence: ")
    List = sentence.split()
    l_word = " "
    for word in List:
        if len(word) > len(l_word):
            l_word = word
    print(l_word)
if __name__=="__main__":
    main()
