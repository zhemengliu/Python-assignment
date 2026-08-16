while True:
    try:
        price = float(input("请输入苹果单价: "))
        quantity = int(input("请输入苹果数量: "))
        total = price * quantity
        print(f"苹果总价为: {total:.2f}元")
        break
    except ValueError:
        print("输入错误！请输入有效的数字。请重新输入！")
