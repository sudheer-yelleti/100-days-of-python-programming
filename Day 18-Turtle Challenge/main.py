# https://docs.python.org/3/contents.html

from turtle import Turtle, Screen
import random

colors = ["red", "green", "blue", "yellow", "orange", "purple", "brown", "pink", "cyan", "black"]
screen = Screen()
screen.screensize(200, 200)

# Draw a square
turtle = Turtle()
for _ in range(4):
    turtle.right(90)
    turtle.forward(100)

# Draw a dashed line
screen.clearscreen()
turtle = Turtle()
for _ in range(10):
    turtle.forward(10)
    turtle.penup()
    turtle.forward(10)
    turtle.pendown()

# Draw different types of polygons
screen.clearscreen()

for i in range(3, 11):
    angle = 360 / i
    turtle = Turtle()
    turtle_color = random.choice(colors)
    turtle.color(turtle_color)

    for j in range(i):
        turtle.right(angle)
        turtle.forward(100)

# Random walk


screen.exitonclick()
