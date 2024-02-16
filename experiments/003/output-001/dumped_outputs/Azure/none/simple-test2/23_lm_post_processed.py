def find_Largest_smallest(numbers):
if not numbers:
return None
Smallest = Largest = numbers[0]
for num in numbers:
if num < Smallest:
Smallest = num
if num > Largest:
Largest = num
return Smallest, Largest
# Example usage.
numbers = [1,2,3, 4,5,6,7,8,9]
result = find_Largest_smallest(numbers)
print(result)
