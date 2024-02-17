input_number = int(input("Enter number"))
val = input_number
result = input_number
while val > 1:
    val = val - 1
    result = result * val
print("factorial for " + str(input_nmb) + " is " + str(result))
