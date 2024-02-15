def filter_string_a(string):
string.sort()
filtered_string_list = []
for stry in string:
if stry.startswith("a"):
filtered_string_list.append(stry)
return filtered_string_list
input_string = ["apple", "banana", "avocado", "cherry", "apricot"]
Output = filter_string_a(input_string)
print(Output)
