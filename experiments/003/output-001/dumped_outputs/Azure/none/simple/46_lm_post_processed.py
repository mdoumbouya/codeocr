def palindromic(stro):
    for i in range(int(len(stro)/2)):
        if stro[i] != stro[len(stro) - i - 1]:
            return False
    return True
