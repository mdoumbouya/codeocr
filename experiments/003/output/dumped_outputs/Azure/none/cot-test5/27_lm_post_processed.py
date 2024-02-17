# Write a Python program to find the longest word in a given text

def main():
sentence = input("Input a sentence: ")
list = sentence.split()
Lword = " "
for word in list:
if len(word) > len(Lword):
Lword = word
print(Lword)
if __name__=="__main__":
main()
