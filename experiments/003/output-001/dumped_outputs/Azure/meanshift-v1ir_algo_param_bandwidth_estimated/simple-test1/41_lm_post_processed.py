def filter_string_a(string):
    string.sort()
    filtered_string_list = []
    for stru in string:
        if stru.startswith("a"):
            filtered_string_list.append(stru)
    return filtered_string_list
input_string = ["apple", "banana", "avocado", "cherry", "apricot"]
output = filter_string_a(input_string)
print(output)
