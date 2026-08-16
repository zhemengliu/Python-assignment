#e3.4DayDayUp365.py
import math
dayup,dayfactor = 1.0,0.01
for i in range(365):
    if i % 7 in [6,0]:
    dayup = math.pow((1.0+dayfactor),365)
    
daydown = math.pow((1.0-dayfactor),365)
print("向上：{:.2f},向下：{:.2f}.".format(dayup,daydown))




