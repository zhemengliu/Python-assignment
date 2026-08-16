class InstanceCreator:
    """演示构造函数和初始化方法的类"""
    special_attr = "类属性"
    
    def __new__(cls, *args, **kwargs):
        """创建实例的构造方法"""
        print("__new__ 正在创建实例")
        instance = super().__new__(cls)
        instance.creation_time = "创建时设置" 
        return instance
    
    def __init__(self, value):
        """实例初始化方法"""
        print("__init__ 正在初始化实例")
        self.value = value
        self.special_attr = "实例属性" 

obj = InstanceCreator(10)
print(f"特殊属性值: {obj.special_attr}")
print(f"创建时添加的属性: {obj.creation_time}")
