import random
import time
import busio
import board
import displayio
import framebufferio
import rgbmatrix
from adafruit_slideshow import SlideShow
import os
from digitalio import DigitalInOut
import pwmio
from digitalio import DigitalInOut, Pull

from config import *
from picomputer import *


slideshow = SlideShow(
    display,
    None,
    folder="/bmps",
    loop=True,
    order=0,
    fade_effect=False,
    dwell=10,
    auto_advance=True,
)

slideshow.brightness=1
while slideshow.update():
    pass


