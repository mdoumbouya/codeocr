seq = [ 1, 2, 3, 4, 5, 6, 7, 8, 9 ]
seq_even=[]
# It checks every element in list (sequence) -
for i in seq:
#it decides whether an element from sequence is even -..
    if i % 2 == 0:
        seq_even.append(i) # appends even ; in empty list (seq_even)
print(seq_even)
