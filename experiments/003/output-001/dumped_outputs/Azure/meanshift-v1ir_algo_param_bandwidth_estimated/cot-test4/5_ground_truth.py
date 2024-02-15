def main():
    num = input("enter the number you want to add")
    sum = 0
    for i in str(num):
        sum = sum + int(i)
    print("sum of the value you entered is", sum)
