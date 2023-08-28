import time
import board
import displayio
import terminalio
from picomputer import *
from math import *
from adafruit_displayio_layout.widgets.cartesian import Cartesian
tick_font = terminalio.FONT

#display = board.DISPLAY  # create the display on the PyPortal or Clue (for example)
# otherwise change this to setup the display
# for display chip driver and pinout you have (e.g. ILI9341)


# Create a Cartesian widget
my_plane = Cartesian(
    x=20,  # x position for the plane
    y=-20,  # y plane position
    width=320,  # display width
    height=240,  # display height
    axes_color=0xFFFF00,  # axes line color
    axes_stroke=2,  # axes lines width in pixels
    tick_color=0x00FFFF,  # ticks color
    major_tick_stroke=1,  # ticks width in pixels
    major_tick_length=5,  # ticks length in pixels
    tick_label_font=tick_font,  # the font used for the tick labels
    font_color=0xFF00FF,  # ticks line color
    xrange=(0, 360),  # x range
    yrange=(0, 100),  # y range
)

my_group = displayio.Group()
my_group.append(my_plane)
display.show(my_group)  # add high level Group to the display

posx = 0
posy = 0
my_plane.add_plot_line(0, 0)
while True:
    for i in range(0, 360, 1):
        my_plane.add_plot_line(i,50+( 30*sin(radians(i))))
        time.sleep(0.001)