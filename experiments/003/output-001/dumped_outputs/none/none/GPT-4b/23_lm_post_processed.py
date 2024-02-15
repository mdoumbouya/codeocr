def find_lrgst_smallest(number):
    if not numbers:
        return None
    smallest = largest = number[0]
    for num in numbers:
        if num < smallest:
            smallest = num
        if num > largest:
            largest = num
    return smallest, largest
#Example usage:
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
result = find_lrgst_smallest(numbers)
print(result)
