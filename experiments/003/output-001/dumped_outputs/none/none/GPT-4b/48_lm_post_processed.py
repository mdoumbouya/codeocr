def fibonacci(n):
    sequence = [0,1]
    i = 0
    while len(sequence) <= n:
        sequence.append(sequence[i+1] + sequence[i+2])
        i += 1
    return sequence
result = fibonacci(6)
print(result)
