def greatest_common_divisor(a,b) :
    smaller_number = a if a < b else b
    common_divisor= []
    for i in range (1, smaller_number +1):
        if 9% i == 0 and 6% i == 0:
            common_divisor.append (i)
    return common_divisor [-1]
