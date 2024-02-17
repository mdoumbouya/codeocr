def greatest_common_divisor(a,b) :
    smaller_number = a if a < b else b
    common_divisor = []
    for i in range (1, smaller_number +1):
        if a % i == 0 and b % i == 0:
            common_divisor.append (i)
    return common_divisor [-1]
