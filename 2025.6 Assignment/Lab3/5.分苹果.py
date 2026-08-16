def distribute_apples():
    try:
        apples = int(input("请输入苹果总数: "))
        children = int(input("请输入小朋友人数: "))
        if apples < children:
            print(f"错误：苹果不够分！只有{apples}个苹果，但有{children}个小朋友。")
        else:
            each = apples // children
            remainder = apples % children
            print(f"每个小朋友分到{each}个苹果，剩余{remainder}个苹果。")
            
    except ValueError:
        print("输入错误！请输入整数。")
    except ZeroDivisionError:
        print("错误：小朋友人数不能为0！")

distribute_apples()
