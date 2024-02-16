upper_lower_count(str):
Upper_case = 0
lower_case = 0
for char in str:
    if char.isupper():
        Upper_case +=1
    else:
        lower_case += 1
return Upper_case, lower_case
