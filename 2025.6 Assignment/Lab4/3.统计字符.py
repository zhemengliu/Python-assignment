import random
import string

random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=1000))

char_count = {}
for char in random_str:
    char_count[char] = char_count.get(char, 0) + 1

for char in sorted(char_count):
    print(f"{char}: {char_count[char]}")
