class StringReprDemo:
    
    def __init__(self, name, value):
        self.name = name
        self.value = value
    
    def __str__(self):
        return f"StringReprDemo: {self.name} (值={self.value})"
    
    def __repr__(self):
        return f"StringReprDemo('{self.name}', {self.value})"


obj = StringReprDemo("测试对象", 42)
print(str(obj))    
print(repr(obj))   
