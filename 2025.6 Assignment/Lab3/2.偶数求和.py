# for循环
sum_for = 0
for i in range(1, 101):
    if i % 2 == 0:
        sum_for += i
print("for循环求和结果:", sum_for)

# while循环
sum_while = 0
i = 1
while i <= 100:
    if i % 2 == 0:
        sum_while += i
    i += 1
print("while循环求和结果:", sum_while)
