students={
    "xiaoyun":"88888",
    "xiaohong":"5555555",
    "xiaoteng":"11111",
    "xiaoyi":"12341234",
    "xiaoyang":"1212121"
    }
print("请输入学生姓名查询QQ号")
name = input()
print(students.get(name,"Not Found"))
