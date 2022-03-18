import time
import board
import busio
import terminalio
import displayio
import gc
import os
import microcontroller
from adafruit_simple_text_display import SimpleTextDisplay

import adafruit_matrixkeypad

from adafruit_st7789 import ST7789
from config import config
import digitalio
hidden_ID = ['.', '_', 'TRASH', 'boot_out.txt', 'main.py', 'code.py', 'menu.py', 'main.txt', 'code.txt', 'boot.py']         # List of file name elements and names we do not want to see
print("--------- STARTING DOS ----------")
print("|   Doomsday Operating System   |")
print("------- Select program ----------")

def file_filter(data):
    for y in hidden_ID:
        filtered_data = [x for x in data if not x.startswith(y)]
        data = filtered_data
    filtered_data = [x for x in data if x[-3:] == '.py' or x[-4:] == '.txt' ]
    return sorted(filtered_data)

menu_options = file_filter(os.listdir())
max_length = len(menu_options)

for i in range(0, max_length, 1):
        print( "[{}] {}".format(i, menu_options[i]))
print("====== Press number 0-9 =========")
while True:

    keypad = adafruit_matrixkeypad.Matrix_Keypad(config.rows, config.cols, config.keys2)
    keys = keypad.pressed_keys
    if keys:
        try:
            selected =int(keys[0])
        except Exception:
            selected = 0

        if selected<max_length:
            exec(open(menu_options[selected]).read())
            print("Program finished ... rebooting ....")
            microcontroller.reset()
