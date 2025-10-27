import turtle
from turtle import Turtle, Screen
import random


def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)


screen = Screen()
screen.setup(width=800, height=600)
screen.colormode(255)
tutle = Turtle()
turtle.speed("fastest")


def draw_spirograph(size_of_gap):
    number_of_circles = int(360 / size_of_gap)

    for _ in range(number_of_circles):
        turtle.color(random_color())
        turtle.circle(100)
        turtle.setheading(turtle.heading() + size_of_gap)


draw_spirograph(7)
screen.exitonclick()
