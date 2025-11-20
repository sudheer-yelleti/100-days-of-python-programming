from turtle import Turtle

MOVE_DISTANCE = 20
SNAKE_LENGTH = 3
UP = 90
LEFT = 180
DOWN = 270
RIGHT = 0


class Snake:

    def __init__(self):
        self.turtle_objects = []
        self.create_snake()
        self.head = self.turtle_objects[0]
        self.head.color("red")

    def create_snake(self):
        initial_position_xaxis = 0
        for i in range(SNAKE_LENGTH):
            new_turtle = Turtle("square")
            new_turtle.color("white")
            new_turtle.penup()
            new_turtle.setposition(initial_position_xaxis, 0)
            initial_position_xaxis -= 20
            self.turtle_objects.append(new_turtle)

    def move(self):
        for turtle_num in range(len(self.turtle_objects) - 1, 0, -1):
            new_x = self.turtle_objects[turtle_num - 1].xcor()
            new_y = self.turtle_objects[turtle_num - 1].ycor()
            self.turtle_objects[turtle_num].goto(new_x, new_y)
        self.head.forward(MOVE_DISTANCE)

    def up(self):
        if self.head.heading() != DOWN:
            self.head.setheading(UP)

    def down(self):
        if self.head.heading() != UP:
            self.head.setheading(DOWN)

    def left(self):
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)

    def right(self):
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)
