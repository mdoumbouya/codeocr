upper_lower_count(str):
upper_case = 0
lower_case = 0
for char in str:
    if char.isupper():
        upper_case +=1
    else:
        lower_case += 1
return upper_case, lower_case
