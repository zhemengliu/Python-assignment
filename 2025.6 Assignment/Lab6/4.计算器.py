class Calculator:
    def __init__(self):
        self.result = 0

    def add(self,a,b):
        self.result = a + b
        return self.result

    def subtract(self,a,b):
        self.result = a - b
        return self.result

    def multiply(self,a,b):
        self.result = a * b
        return self.result

    def divide(self,a,b):
        if b==0:
            raise ValueError("除数不能为0")
        self.result = a / b
        return self.result

calc = Calculator()
print(calc.add(2, 5))      
print(calc.subtract(10, 3))   
print(calc.multiply(3, 4))  
print(calc.divide(15, 3))
    
