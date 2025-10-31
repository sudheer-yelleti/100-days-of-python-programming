# Listener events
from turtle import Turtle, Screen

turtle = Turtle()

screen = Screen()
screen.colormode(255)
screen.listen()


def move_forward():
    turtle.forward(10)


def move_backward():
    turtle.backward(10)


def move_left():
    turtle.left(90)


def move_right():
    turtle.right(90)


def clear_screen():
    turtle.clear()
    turtle.penup()
    turtle.setposition(0, 0)
    turtle.pendown()


screen.onkey(fun=move_forward, key="W")
screen.onkey(fun=move_backward, key="S")
screen.onkey(fun=move_left, key="A")
screen.onkey(fun=move_right, key="D")
screen.onkey(fun=clear_screen, key="C")

screen.exitonclick()
