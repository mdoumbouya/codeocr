def main():
    string = str(input("Enter string: "))
    for i in range((len(string)-1), -1, -1):
        print(string[i])
    if __name__ == '__main__':
        main()
