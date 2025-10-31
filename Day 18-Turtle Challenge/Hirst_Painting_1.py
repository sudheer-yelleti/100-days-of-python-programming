import random
import turtle as t

import colorgram

# Extract 5 colors from the image
colors = colorgram.extract('image.jpg', 30)

rgb_colors = []
screen = t.Screen()
screen.colormode(255)
for color in colors:
    r = color.rgb.r
    g = color.rgb.g
    b = color.rgb.b
    if (r < 240 and g < 240 and b < 240):
        new_color = (r, g, b)
        rgb_colors.append(new_color)

print(rgb_colors)

t.hideturtle()
t.speed("fastest")
t.penup()
t.goto(-250, -250)

for i in range(1, 101):
    t.dot(20, random.choice(rgb_colors))
    t.forward(50)

    if i % 10 == 0:
        t.left(90)
        t.forward(50)
        t.left(90)
        t.forward(500)
        t.right(180)

t.exitonclick()
