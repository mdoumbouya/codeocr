def main():
list1 = [1, 2,3,4]
list2 = (3,4,5,6)
List = []
for elem1 in list1:
for elem2 in list2:
if elem1 == elem2:
elem = elem2
List.append(elem)
print(List)
