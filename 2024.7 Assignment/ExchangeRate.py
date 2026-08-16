#Practice2.2_ExchangeRate
Money = input("请输入带符号的金钱值：")
if Money[-1] in ['R','r']:
    Dollor=eval(Money[0:-1])*6
    print("转换后的金钱值为{:.2f}$".format(Dollor))
elif Money[-1] in '$':
    Rmb=eval(Money[0:-1])/6
    print("转换后的金钱值为{:.2f}R".format(Rmb))
else:
    print("输入的格式错误")
