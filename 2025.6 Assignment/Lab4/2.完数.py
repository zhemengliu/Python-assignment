for num in range(2, 1001):
    factors = [1]
    for i in range(2, num):
        if num % i == 0:
            factors.append(i)
    if sum(factors) == num:
        print(num)
