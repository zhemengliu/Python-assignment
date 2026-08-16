class ResourceHandler:
    
    def __init__(self, resource_name):
        self.resource_name = resource_name
        print(f"获取资源: {self.resource_name}")
    
    def __del__(self):
        print(f"释放资源: {self.resource_name}")

def use_resource():    print("创建临时资源")
    temp = ResourceHandler("临时文件")
    print("使用资源中...")

print("程序开始")
use_resource()
print("函数执行完毕")

import gc
gc.collect()
print("程序结束")
