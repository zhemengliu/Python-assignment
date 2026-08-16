#Practice2.8 正方形螺线
import turtle
turtle.setup(600,600,300,300)
turtle.pendown()
turtle.pensize(3)
turtle.pencolor("black")
turtle.seth(90)
for i in range(5,300,5):
    turtle.seth(i*18)
    turtle.fd(i)
