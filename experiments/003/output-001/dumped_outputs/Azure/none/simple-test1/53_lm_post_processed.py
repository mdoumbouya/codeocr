upper_lower_count(sto):
Upper_case = 0
lower_case = 0
for char in sto:
if char.isupper():
Upper_case +=1
else:
lower_case += 1
return Upper_case, lower_case
