num = int(input("Enter a number: "))
ans = 1
while num > 1:
    ans*= num
    num -= 1
print(ans)
