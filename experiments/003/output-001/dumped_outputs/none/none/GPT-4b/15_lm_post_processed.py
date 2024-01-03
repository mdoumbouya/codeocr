def main():
    lst1 = [1,2,3]
    lst2 = [3,4,5]
    lst = []
    for elem1 in lst1:
        for elem2 in lst2:
            if elem1 == elem2:
                elem = elem1 + elem2
                lst.append(elem)
    print(lst)
