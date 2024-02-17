def palindromic(str):
    for i in range(int(len(str) / 2)):
        if str[i] != str[len(str) - i]:
            return False
    return True
