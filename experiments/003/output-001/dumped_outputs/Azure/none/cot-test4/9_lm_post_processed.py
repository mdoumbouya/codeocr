def main():
vowel_count=0
vowels=['a' ,'e' ,'i','o', 'u']
input_string = input ("Enter the string:")
input_string = input_string . lower ()
for char in input_string:
for vowel in vowels :
if char == vowel:
vowel_count+=1
print(vowel_count)
if __name__ == '__main__' :
main ( )
