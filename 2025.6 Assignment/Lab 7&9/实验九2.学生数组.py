import pandas as pd

def create_student_data():
    students = [
        ["学号", "姓名", "年龄", "性别", "成绩"],
        [1001, "A", 11, "男", 12],
        [1002, "B", 12, "女", 22],
        [1003, "C", 13, "女", 32],
        [1004, "D", 14, "男", 52]
    ]
    
    df = pd.DataFrame(students[1:], columns=students[0])
    
    df.to_excel('test.xlsx', index=False)
    
    print("Excel文件已创建：test.xlsx")
    return df

student_df = create_student_data()

print("\nExcel文件内容预览:")
print(student_df)
