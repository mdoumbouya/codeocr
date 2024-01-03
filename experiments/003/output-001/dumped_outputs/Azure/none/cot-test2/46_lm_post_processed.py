def palindroomic (stro):
for i in range (int (len(stro)/2)):
if stro [i] != stro [len (stro) -i]:
return False
return True
