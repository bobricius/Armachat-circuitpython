# SPDX-FileCopyrightText: 2020 Tim C, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""
PyPortal implementation of Busy Simulator notification sound looper.
"""
import time
import board
from adafruit_displayio_layout.layouts.grid_layout import GridLayout
from adafruit_displayio_layout.widgets.icon_widget import IconWidget

from adafruit_cursorcontrol.cursorcontrol import Cursor
from picomputer import *

# How many seconds to wait between playing samples
# Lower time means it will play faster
WAIT_TIME = 3.0

# List that will hold indexes of notification samples to play
LOOP = []

# last time that we played a sample
LAST_PLAY_TIME = 0

CUR_LOOP_INDEX = 0

# touch events must have at least this long between them
COOLDOWN_TIME = 0.25  # seconds

# last time that the display was touched
# used for debouncing and cooldown enforcement
LAST_PRESS_TIME = -1

# Was any icon touched last iteration.
# Used for debouncing.
WAS_TOUCHED = False


def next_index():
    """
    return the next index in the LOOP that should get played
    """
    if CUR_LOOP_INDEX + 1 >= len(LOOP):
        return 0

    return CUR_LOOP_INDEX + 1


# list of icons to show
# each entry is a tuple containing:
# (Icon Label, Icon BMP image file, Notification sample wav file
_icons = [
    ("Home", "icons/Home.bmp", "sounds/outlook.wav"),
    ("Time", "icons/Time.bmp", "sounds/phone.wav"),
    ("Armachat", "icons/Phone.bmp", "sounds/skype.wav"),
    ("Tourtle", "icons/Turtle.bmp", "sounds/teams.wav"),
    ("Keyboard", "icons/Keyboard.bmp", "sounds/discord.wav"),
    ("Games", "icons/Games.bmp", "sounds/applemail.wav"),
    ("Calculator", "icons/Abacus.bmp", "sounds/imessage.wav"),
    ("Temperature", "icons/Thermometer.bmp", "sounds/slack.wav"),
    ("Language", "icons/Flag.bmp", "sounds/RE.wav"),
    ("Photoframe", "icons/Multimedia.bmp", "sounds/gchat.wav"),
    ("REPL", "icons/Tax.bmp", ""),
]

# Make the display context.
#display = board.DISPLAY
main_group = displayio.Group()
display.show(main_group)


# Setup the file as the bitmap data source
bg_bitmap = displayio.OnDiskBitmap("/bmps/desktop.bmp")

# Create a TileGrid to hold the bitmap
bg_tile_grid = displayio.TileGrid(
    bg_bitmap,
    pixel_shader=getattr(bg_bitmap, "pixel_shader", displayio.ColorConverter()),
)

# add it to the group that is showing
main_group.append(bg_tile_grid)



# grid to hold the icons
layout = GridLayout(
    x=0,
    y=0,
    width=320,
    height=240,
    grid_size=(4, 3),
    cell_padding=1,
)

# initialize the icons in the grid
for i, icon in enumerate(_icons):
    icon_widget = IconWidget(
        icon[0],
        icon[1],
        x=0,
        y=0,
        on_disk=False,
        transparent_index=6,
        label_background=0x000000,
    )

    layout.add_content(icon_widget, grid_position=(i % 4, i // 4), cell_size=(1, 1))

# add the grid to the group showing on the display
main_group.append(layout)


def check_for_click(x,y):
    # loop over the icons
    for _ in range(len(_icons)):
        # lookup current icon in the grid layout
        cur_icon = layout.get_cell((_ % 4, _ // 4))

        # check if it's being touched
        if cur_icon.contains((mouse_cursor.x, mouse_cursor.y)):
            print("icon {} click".format(_))
            print("playing: {}".format(_icons[_][2]))
            beep()
            
            # if it's the stop icon
            if _icons[_][0] == "Stop":
                ring()





# initialize the mouse cursor object
mouse_cursor = Cursor(display, display_group=main_group)

# main loop
x=100
y=100

while True:
#    cursor.update()
    keys=getKey(0)
    if keys:
        if keys == "lt":
            if x > 0:
                x = x - 1
        if keys == "rt":
            if x < 320:
                x = x + 1
        if keys == "up":
            if y > 0:
                y = y - 1
        if keys == "dn":
            if y < 240:
                y = y + 1
        if keys == "ent":
            check_for_click(x,y)
            
    mouse_cursor.x=x
    mouse_cursor.y=y

#while True: