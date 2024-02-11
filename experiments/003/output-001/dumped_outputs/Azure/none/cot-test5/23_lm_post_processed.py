def find_largest_smallest(number):
if not numbers:
Return none
Smallest= largest = number[0]
for num in numbers:
if num < Smallest:
Smallest = num
if num > largest:
Largest = num
return Smallest, Largest
# Example usage.
numbers = [1,2,3, 4,5,6,7,8,9]
result = find_largest_smallest(numbers)
print(result)
