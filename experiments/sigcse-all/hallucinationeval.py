import pandas as pd

data = pd.read_csv('SIGCSE Final Data 2023-08-16 - Hallucination.csv')



def reset_count():
    count = {}
    count['No Change'] = 0
    count['Small Change in the Comment'] = 0
    count['Missed Something From Ground Truth'] = 0
    count['Print Statement Change'] = 0
    count['Added code that was not present'] = 0
    count['Small Variable/Function Name Change'] = 0
    count['Small Change in the Indentation'] = 0
    count['Small Syntax Fix'] = 0
    count['Logical Fix'] = 0
    return count



data1 = data['Change Category Double Prompting'].tolist()
data2 = data['Change Category Low'].tolist()
data3 = data['Change Category Medium'].tolist()
data4 = data['Change Category High'].tolist()

full_data = []
full_data.append(data1)
full_data.append(data2)
full_data.append(data3)
full_data.append(data4)

for data in full_data:
    count = reset_count()
    for elem in data:
        if elem not in count:
            count[elem] = 1
        else:
            count[elem] += 1
            

    sorted_count = sorted(count.items(), key=lambda x:x[1], reverse=True)

    sorted_count = dict(sorted_count)


    total = sum(count.values())

    print('\n')
    # Printing how many times each category appeared in the dataset

    for elem in sorted_count:
        print("-----------------------------------------------------------------------------------------------------------------")
        print(f"Category: {elem} || Frequency: {sorted_count[elem]}   || Percentage: {round(sorted_count[elem]/total * 100, 2)}%")
        print("-----------------------------------------------------------------------------------------------------------------")
        print("\n")

    print("---------------")
    print(f"n = {total}")
    print("---------------")
