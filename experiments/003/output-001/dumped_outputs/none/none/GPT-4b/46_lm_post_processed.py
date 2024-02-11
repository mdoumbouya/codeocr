def palindromic(stro):
    for i in range(int(len(stro)/2)):
        if stro[i] != str[len(stro)-i]:
            return False
    return True
