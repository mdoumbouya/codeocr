def main():
    list1 = [[1, 2], [3, 4]]
    list2 = [5, 6, 7, 8]
    for elem1 in list1:
        for elem2 in list2:
            if elem1[1] == elem2:
                list2.remove(elem2)
    list1.append(list2)
print(list1)
