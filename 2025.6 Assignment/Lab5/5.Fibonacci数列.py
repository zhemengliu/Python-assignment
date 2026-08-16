# 递归
def fib_digui(n):
    if n <= 2:
        return 1
    return fib_digui(n-1) + fib_digui(n-2)

# 非递归
def fib_feidigui(start, end):
    a, b = 1, 1
    fibs = []
    while a <= end:
        if a >= start:
            fibs.append(a)
        a, b = b, a + b
    return fibs

# main
def fibonacci_range():
    start = int(input("输入起始数(1-10000): "))
    end = int(input("输入结束数(1-10000): "))
    
    fibs = fib_feidigui(start, end)
    print(f"非递归结果({start}-{end}): {fibs}")
    
    fibs_dg = []
    n = 1
    while True:
        fib = fib_digui(n)
        if fib > end:
            break
        if fib >= start:
            fibs_dg.append(fib)
        n += 1
    print(f"递归结果({start}-{end}): {fibs_dg}")

fibonacci_range()
