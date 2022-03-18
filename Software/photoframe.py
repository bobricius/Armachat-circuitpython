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
from adafruit_display_text import label
from adafruit_st7789 import ST7789
from digitalio import DigitalInOut, Pull

#, board.IO3
displayio.release_displays()

tft_cs = board.GP21
tft_dc = board.GP16
spi_mosi = board.GP19
spi_clk = board.GP18
spi = busio.SPI(spi_clk, spi_mosi)
backlight = board.GP20

#BACKLIGHT = PWMOut(backlightLed, duty_cycle=0, frequency=500, variable_frequency=True)
#BACKLIGHT.duty_cycle = 65535

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)

display = ST7789(display_bus, rotation=270, width=320, height=240, backlight_pin=backlight)
# Make the display context
splash = displayio.Group()
display.show(splash)

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


