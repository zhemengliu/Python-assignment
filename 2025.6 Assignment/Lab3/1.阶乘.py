#1.求数的阶乘
def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result
try:
    num = int(input("请输入一个正整数: "))
    if num < 0:
        print("输入错误：请输入正整数！")
    else:
        print(f"{num}的阶乘是: {factorial(num)}")
except ValueError:
    print("输入错误：请输入一个整数！")
