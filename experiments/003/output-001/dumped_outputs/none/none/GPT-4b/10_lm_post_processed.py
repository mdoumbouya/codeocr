def main():
    string = str(input('Enter a string:'))
    for i in range(len(string)-1, -1, -1):
        print(string[i])
