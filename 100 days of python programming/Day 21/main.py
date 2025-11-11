import time
import tkinter as tk
from turtle import Screen

from food import Food
from scoreboard import Scoreboard
from snake import Snake

root = tk.Tk()
screen_height = root.winfo_screenheight()
screen_width = root.winfo_screenwidth()
root.destroy()

screen = Screen()
screen.setup(width=screen_width, height=screen_height)

screen.bgcolor("black")
screen.title("My Snake Game")
screen.tracer(0)

snake = Snake()
food = Food()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(fun=snake.up, key="Up")
screen.onkey(fun=snake.down, key="Down")
screen.onkey(fun=snake.left, key="Left")
screen.onkey(fun=snake.right, key="Right")

is_game_on = True
while is_game_on:
    screen.update()
    time.sleep(0.1)
    snake.move()

    # Detect collision with food.
    if snake.head.distance(food) < 15:
        food.move_to_random_position()
        scoreboard.increase_score()
        snake.extend()

    # Detect collision with the wall.
    if (snake.head.xcor() >= screen_width / 2 or snake.head.xcor() <= -(screen_width / 2)):
        is_game_on = False
        scoreboard.game_over()
    elif (snake.head.ycor() >= screen_height / 2 or snake.head.ycor() <= -(screen_height / 2)):
        is_game_on = False
        scoreboard.game_over()
    # Detect collision with the snake's tail.
    for snake_segment in snake.turtle_objects[1:]:
        if snake.head.distance(snake_segment) < 10:
            is_game_on = False
            scoreboard.game_over()

screen.exitonclick()
