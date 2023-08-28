import board
from picomputer import *

from adafruit_turtle import Color, turtle

turtle = turtle(display)
starsize = min(display.width, display.height) * 0.5  # 90% of screensize
benzsize = min(display.width, display.height) * 0.5  # 90% of screensize

print("Turtle time! Lets draw a star")

turtle.pencolor(Color.BLUE)

turtle.penup()
turtle.goto(0, 0)
turtle.pendown()

start = turtle.pos()
while True:
    turtle.forward(starsize)
    turtle.left(170)
    if abs(turtle.pos() - start) < 1:
        break

#turtle.clear()

colors = (Color.RED, Color.ORANGE, Color.YELLOW, Color.GREEN, Color.BLUE, Color.PURPLE)

turtle.pendown()
start = turtle.pos()

for x in range(benzsize):
    turtle.pencolor(colors[x%6])
    turtle.forward(x)
    turtle.left(59)


def hilbert2(step, rule, angle, depth, t):
    if depth > 0:
        a = lambda: hilbert2(step, "a", angle, depth - 1, t)
        b = lambda: hilbert2(step, "b", angle, depth - 1, t)
        left = lambda: t.left(angle)
        right = lambda: t.right(angle)
        forward = lambda: t.forward(step)
        if rule == "a":
            left(); b(); forward(); right(); a(); forward(); a(); right(); forward(); b(); left()
        if rule == "b":
            right(); a(); forward(); left(); b(); forward(); b(); left(); forward(); a(); right()

#turtle.clear()

turtle.penup()

turtle.goto(0, 0)
turtle.pendown()
hilbert2(5, "a", 90, 5, turtle)