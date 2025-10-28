import random
from random import shuffle
from turtle import Turtle, Screen
import tkinter

colors = ["violet", "indigo", "blue", "green", "yellow", "orange", "red"]
turtle_objects = []
screen = Screen()
screen_height = screen.window_height()
screen_width = screen.window_width()
screen.setup(width=screen_width, height=screen_height)
is_race_on = False

user_bet = screen.textinput(title="Guess the winner", prompt="Which turtle will win the race? Enter the color: ")

height = (-screen_height / 4) + 80
width = -(screen_width / 2) + 20
print(screen_height, screen_width)
for i in range(len(colors)):
    new_turtle = Turtle("turtle")
    new_turtle.penup()
    new_turtle.color(colors[i])
    new_turtle.speed("fast")
    turtle_objects.append(new_turtle)
    new_turtle.goto(width, height)
    height += 50

if user_bet:
    is_race_on = True
while is_race_on:
    for turtle in turtle_objects:
        turtle.forward(random.randint(0, 10))
        if (turtle.xcor() > (screen_width / 2) - 28):
            is_race_on = False
            winning_turtle_color = turtle.pencolor()
            msg = Turtle()
            msg.hideturtle()
            msg.penup()
            msg.goto(0, 0)
            if user_bet.lower() == winning_turtle_color.lower():
                msg.write(f"🎉 You won! The winner is {winning_turtle_color}.", align="center",
                          font=("Arial", 24, "bold"))
            else:
                msg.write(f"😞 You lost! The winner is {winning_turtle_color}.", align="center",
                          font=("Arial", 24, "bold"))

screen.exitonclick()
