import time
import board
import busio
import gc
import terminalio
import displayio
import microcontroller
import storage


from digitalio import DigitalInOut

from adafruit_display_text import label
from adafruit_st7789 import ST7789

# Release any resources currently in use for the displays
displayio.release_displays()

tft_cs = board.GP21
tft_dc = board.GP16

spi_mosi = board.GP19
spi_clk = board.GP18
spi = busio.SPI(spi_clk, spi_mosi)
backlight = board.GP20

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)

display = ST7789(
    display_bus, rotation=270, width=320, height=240, backlight_pin=backlight
)

# Make the display context
# splash = displayio.Group()
# display.show(splash)

print ("Free memory:")
print (gc.mem_free())
print ("Starting code.py...")

