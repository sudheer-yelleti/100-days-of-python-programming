import random
from turtle import Turtle, Screen


def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)


directions = [0, 90, 180, 270]
distance_to_move = 30
screen = Screen()
screen.colormode(255)

turtle = Turtle()
turtle.pensize(5)
turtle.speed("fastest")
for _ in range(200):
    direction = random.choice(directions)
    turtle.color(random_color())
    turtle.forward(distance_to_move)
    turtle.setheading(direction)
