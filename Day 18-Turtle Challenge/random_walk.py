import random
from turtle import Turtle

colors = ["red", "green", "blue", "yellow", "orange", "purple", "brown", "pink", "cyan", "black"]
directions = [0, 90, 180, 270]
distance_to_move = 30

turtle = Turtle()
turtle.pensize(5)
turtle.speed("fastest")
for _ in range(200):
    direction = random.choice(directions)
    turtle.color(random.choice(colors))
    turtle.forward(distance_to_move)
    turtle.setheading(direction)
