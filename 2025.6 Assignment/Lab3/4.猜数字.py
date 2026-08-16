import random

def guess_number():
    number = random.randint(1, 100)
    attempts = 5
    for attempt in range(1, attempts + 1):
        try:
            guess = int(input(f"\n第{attempt}次尝试，请输入你的猜测: "))
            
            if guess < number:
                print(f"太小了。")
            elif guess > number:
                print(f"太大了。")
            else:
                print(f"恭喜你！第{attempt}次尝试时猜对了数字{number}！")
                return True
                
        except ValueError:
            print("请输入有效的整数！")
            
    print(f"\n很遗憾，5次机会已用完！正确答案是: {number}")
    return False

if guess_number():
    print("游戏成功！")
else:
    print("游戏失败！")
