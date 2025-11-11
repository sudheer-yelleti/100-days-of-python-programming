import time
from turtle import Screen

from ball import Ball
from paddle import Paddle
from scoreboard import Scoreboard

screen_height = 600
screen_width = 800

screen = Screen()

screen.setup(width=screen_width, height=screen_height)
screen.bgcolor("black")
screen.title("Pong")
screen.listen()
screen.tracer(0)

r_paddle = Paddle((screen_width / 2 - 20, 0))
l_paddle = Paddle((-screen_width / 2 + 20, 0))
ball = Ball()
scoreboard = Scoreboard()

screen.onkey(key="Up", fun=r_paddle.paddle_up)
screen.onkey(key="Down", fun=r_paddle.paddle_down)
screen.onkey(key="w", fun=l_paddle.paddle_up)
screen.onkey(key="s", fun=l_paddle.paddle_down)

is_game_on = True
while is_game_on:
    time.sleep(ball.move_speed)
    screen.update()
    ball.move()

    # Detect ball's collision with the top wall
    if ball.ycor() > screen_height / 2 - 20 or ball.ycor() < -screen_height / 2 + 20:
        ball.bounce_y()
    # Detect collision with the right paddle
    if ball.distance(r_paddle) < 50 and ball.xcor() > 320 or ball.distance(l_paddle) < 50 and ball.xcor() < -320:
        ball.bounce_x()

    if ball.xcor() > screen_width / 2:
        scoreboard.l_point()
        ball.reset_position()

    if ball.xcor() < -screen_width / 2:
        scoreboard.r_point()
        ball.reset_position()

    if scoreboard.l_score == Scoreboard.WINNING_SCORE or scoreboard.r_score == Scoreboard.WINNING_SCORE:
        is_game_on = False
        scoreboard.game_over()

screen.exitonclick()
