# 1. filter() 过滤偶数
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
even = filter(lambda x: x % 2 == 0, numbers)
print("偶数:", list(even))  

# 2. map() 计算平方
squares = map(lambda x: x**2, numbers)
print("平方:", list(squares)) 

# 3. sorted() 按字符串长度排序
words = ["apple", "banana", "cherry", "date"]
sorted_words = sorted(words, key=lambda x: len(x))
print("按长度排序:", sorted_words)
