def main():
    num = input("enter the number you want to add: ")
    Sum = 0
    for i in str(num):
        Sum = Sum + int(i)
    print("sum of the value you entered is", Sum)
    return
