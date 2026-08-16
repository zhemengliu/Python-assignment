def shuixian():
    results = []
    print("水仙花数有:")
    for num in range(100,1000):
        h=num//100
        t=(num//10)%10
        u=num%10
        if h**3+t**3+u**3==num:
            results.append(str(num))
    output=", ".join(results)
    print(output)

shuixian()
