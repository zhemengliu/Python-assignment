import math
class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def calculate_distance(self,other_point):
        return math.sqrt((self.x - other_point.x)**2 + (self.y - other_point.y)**2)

p1 = Point(3,4)
p2 = Point(0,0)
print(p1.calculate_distance(p2))
    
