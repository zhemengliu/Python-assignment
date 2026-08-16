class ModuleDemo:
    @staticmethod
    def main_logic():
        print("模块作为主程序运行")

if __name__ == "__main__":
    print("当前模块运行成功")
    ModuleDemo.main_logic()
else:
    print(f"当前模块被导入为: {__name__}")
