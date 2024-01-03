def filter_string_a(string):
string.sort()
filtered_string_list = []
for str in string:
if str.startswith("a"):
filtered_string_list.append(str)
return filtered_string_list
input_string = ["apple", "banana", "avocado", "cherry", "apricot"]
Output = filter_string_a(input_string)
print(Output)
