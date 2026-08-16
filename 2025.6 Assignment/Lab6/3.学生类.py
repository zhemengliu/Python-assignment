class Student():
    def __init__(self,name,age,grades):
        self.name = name
        self.age = age
        self.grades = grades

    def display_info(self):
        print(f"姓名：{self.name}")
        print(f"年龄：{self.age}")
        print(f"成绩：{self.grades}")
        for subject, score in self.grades.items():
            print(f"  {subject}: {score}")

student = Student("张三", 18, {"数学": 95, "语文": 88, "英语": 92})
student.display_info()
