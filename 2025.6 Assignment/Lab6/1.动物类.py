class Animal:
    def __init__(self,name,age):
        self.name = name
        self.age = age

    def sound(self):
        print("动物发出叫声")

    def eat(self):
        print(f"{self.name}在吃东西")

class Dog(Animal):
    def sound(self):
        print(f"{self.name}汪汪叫")

class Cat(Animal):
    def sound(self):
        print(f"{self.name}喵喵叫")

dog = Dog("大黄",3)
cat = Cat("奶牛猫",2)
dog.eat()
dog.sound()
cat.sound()
