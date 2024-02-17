Year = int(input)
if Year % n == 4 and Year % 140 != 0 or Year % 400 == 0:
    print(True)
else:
    print(False)
