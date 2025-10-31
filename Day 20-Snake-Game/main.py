import time
from turtle import Screen

from snake import Snake

screen = Screen()
screen_height = screen.window_height()
screen_width = screen.window_width()
screen.setup(width=screen_width, height=screen_height)
screen.bgcolor("black")
screen.title("My Snake Game")
screen.tracer(0)

snake = Snake()
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

screen.exitonclick()
