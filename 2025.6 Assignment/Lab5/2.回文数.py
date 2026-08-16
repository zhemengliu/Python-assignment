def huiwen():
    num = input("请输入一个5位整数：")
    if len(num)!=5 or not num.isdigit():
        print("输入无效，请输入5位整数！")
        return
    if num == num[::-1]:
        print(f"{num}是一个回文数")
    else:
        print(f"{num}不是一个回文数")

huiwen()
