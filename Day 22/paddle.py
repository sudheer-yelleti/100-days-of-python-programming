from turtle import Turtle

PADDLE_MARGIN = 240
PADDLE_MOVE_DISTANCE = 60


class Paddle(Turtle):
    def __init__(self, position):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_len=1, stretch_wid=5)
        self.penup()
        self.goto(position)

    def paddle_up(self):
        if self.ycor() < PADDLE_MARGIN:
            new_y = self.ycor() + PADDLE_MOVE_DISTANCE
            self.goto(self.xcor(), new_y)

    def paddle_down(self):
        if self.ycor() > -PADDLE_MARGIN:
            new_y = self.ycor() - PADDLE_MOVE_DISTANCE
            self.goto(self.xcor(), new_y)
