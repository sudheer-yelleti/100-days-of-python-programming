import time
from turtle import Screen, Turtle

screen = Screen()
screen_height = screen.window_height()
screen_width = screen.window_width()
screen.setup(width=screen_width, height=screen_height)
screen.bgcolor("black")
screen.title("My Snake Game")
screen.tracer(0)
turtle_objects = []

initial_position_xaxis = 0

for i in range(3):
    new_turtle = Turtle("square")
    new_turtle.color("white")
    new_turtle.penup()
    new_turtle.setposition(initial_position_xaxis, 0)
    initial_position_xaxis -= 20
    turtle_objects.append(new_turtle)

is_game_on = True
while is_game_on:
    screen.update()
    time.sleep(0.1)

    for turtle_num in range(len(turtle_objects) - 1, 0, -1):
        new_x = turtle_objects[turtle_num - 1].xcor()
        new_y = turtle_objects[turtle_num - 1].ycor()
        turtle_objects[turtle_num].goto(new_x, new_y)
    turtle_objects[0].forward(20)

screen.update()

screen.exitonclick()
