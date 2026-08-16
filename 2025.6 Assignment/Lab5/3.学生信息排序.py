def student_info():
    print("请输入学生信息:学号 姓名（每行一个学生，输入空行结束）")
    students = {}
    
    while True:
        line = input().strip()
        if not line:  
            break
        parts = line.split()
        if len(parts) >= 2:
            sid = parts[0]
            name = ' '.join(parts[1:])
            students[sid] = name
    
    # 按学号升序排序
    sorted_by_id = sorted(students.items(), key=lambda x: x[0])
    print("\n按学号升序：")
    for sid, name in sorted_by_id:
        print(f"学号：{sid}, 姓名：{name}")
    
    # 按姓名首字母升序排序
    sorted_by_name = sorted(students.items(), key=lambda x: x[1])
    print("\n按姓名首字母升序：")
    for sid, name in sorted_by_name:
        print(f"学号：{sid}, 姓名：{name}")

student_info()
