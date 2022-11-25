import time
import board
import busio
import digitalio
import os
import displayio
import microcontroller
from pwmio import PWMOut
from adafruit_st7789 import ST7789
from adafruit_st7735r import ST7735R
import supervisor

#------------configure your device----------------

#------------configure keyboard----------------
keyboard_model="keys36"
#keyboard_model="keys30"
#keyboard_model="keys30watch"
#------------configure display----------------
display_model= "display320x240"
#display_model= "display160x80"
#------------configure Radio module connection ----------------
model_lora = "compact"
#model_lora = "watch"

#LoRa radio configuration
country = "EU"
lora_preset = "long/short"
frequency = 869.525
signal_bandwidth =125000
coding_rate = 8
spreading_factor = 10
preamble_length = 32
tx_power = 10

# Communicator
myName = "bobricius"
#my address
adrFrom3 = 192
adrFrom2 = 168
adrFrom1 = 0
adrFrom0 = 1
#destination
adrTo3 = 192
adrTo2 = 168
adrTo1 = 0
adrTo0 = 2
#message counter
msgId3 = 255
msgId2 = 255
msgId1 = 255
msgId0 = 0
# Encryption password
password = "Sixteen byte key"
passwordIv = "Sixteen byte key"

#display
MAX_INPUT_TEXT = 240
volume = 6


if keyboard_model == "keys30":
    cols = [
        digitalio.DigitalInOut(x)
        for x in (board.GP1, board.GP2, board.GP3, board.GP4, board.GP5)
    ]
    rows = [
        digitalio.DigitalInOut(x)
        for x in (board.GP6, board.GP9, board.GP15, board.GP8, board.GP7, board.GP22)
    ]
    keys1 = (
        ("ent", " ", "m", "n", "b"),
        ("bsp", "l", "k", "j", "h"),
        ("p", "o", "i", "u", "y"),
        ("alt", "z", "x", "c", "v"),
        ("a", "s", "d", "f", "g"),
        ("q", "w", "e", "r", "t"),
    )

    keys2 = (
        ("rt", ",", ">", "<", '""'),
        ("lt", "-", "*", "&", "+"),
        ("0", "9", "8", "7", "6"),
        ("alt", "(", ")", "?", "/"),
        ("!", "@", "#", "$", "%"),
        ("1", "2", "3", "4", "5"),
    )

    keys3 = (
        ("dn", ";", "M", "N", "B"),
        ("up", "L", "K", "J", "H"),
        ("P", "O", "I", "U", "Y"),
        ("alt", "Z", "X", "C", "V"),
        ("A", "S", "D", "F", "G"),
        ("Q", "W", "E", "R", "T"),
    )

elif keyboard_model == "keys36":
    #Display configuration
    cols = [
        digitalio.DigitalInOut(x)
        for x in (board.GP1, board.GP2, board.GP3, board.GP4, board.GP5, board.GP14)
    ]
    rows = [
        digitalio.DigitalInOut(x)
        for x in (board.GP6, board.GP9, board.GP15, board.GP8, board.GP7, board.GP22)
    ]
    keys1 = (
        (" ", ".", "m", "n", "b", "dn"),
        ("ent", "l", "k", "j", "h", "lt"),
        ("p", "o", "i", "u", "y", "up"),
        ("bsp", "z", "x", "c", "v", "rt"),
        ("a", "s", "d", "f", "g", "tab"),
        ("q", "w", "e", "r", "t", "alt"),
    )

    keys2 = (
        ("_", ",", ">", "<", '""', "{"),
        ("~", "-", "*", "&", "+", "["),
        ("0", "9", "8", "7", "6", "}"),
        ("=", "(", ")", "?", "/", "]"),
        ("!", "@", "#", "$", "%", "\\"),
        ("1", "2", "3", "4", "5", "alt"),
    )

    keys3 = (
        (":", ";", "M", "N", "B", "dn"),
        ("ent", "L", "K", "J", "H", "lt"),
        ("P", "O", "I", "U", "Y", "up"),
        ("bsp", "Z", "X", "C", "V", "rt"),
        ("A", "S", "D", "F", "G", "tab"),
        ("Q", "W", "E", "R", "T", "alt"),
    )

elif keyboard_model == "keys30watch":
    # Setup Keyboard
    cols = [
        digitalio.DigitalInOut(x)
        for x in (board.GP28, board.GP27, board.GP26, board.GP22, board.GP21)
    ]
    rows = [
        digitalio.DigitalInOut(x)
        for x in (
                board.GP20, board.GP19, board.GP18, board.GP17, board.GP16, board.GP15
            )
    ]
    keys1 = (
        ("ent", " ", "m", "n", "b"),
        ("bsp", "l", "k", "j", "h"),
        ("p", "o", "i", "u", "y"),
        ("alt", "z", "x", "c", "v"),
        ("a", "s", "d", "f", "g"),
        ("q", "w", "e", "r", "t"),
    )
    keys2 = (
        ("rt", ",", ">", "<", '""'),
        ("lt", "-", "*", "&", "+"),
        ("0", "9", "8", "7", "6"),
        ("alt", "(", ")", "?", "/"),
        ("!", "@", "#", "$", "%"),
        ("1", "2", "3", "4", "5"),
    )
    keys3 = (
        ("dn", ";", "M", "N", "B"),
        ("up", "L", "K", "J", "H"),
        ("P", "O", "I", "U", "Y"),
        ("alt", "Z", "X", "C", "V"),
        ("A", "S", "D", "F", "G"),
        ("Q", "W", "E", "R", "T"),
    )


# ----------         End of Keyboard Settings          ----------



#------------configure Radio module connection ----------------
#model_lora = "compact"
#model_lora = "watch"



if model_lora == "compact":
    #Lora HW configuration MAX
    LORA_CS = digitalio.DigitalInOut(board.GP13)
    LORA_SCK = board.GP10
    LORA_MOSI = board.GP11
    LORA_MISO = board.GP12
    # Setup Speaker/Buzzer
    AUDIO_GPIO = board.GP0
     
elif model_lora == "watch":
    #Lora HW configuration WATCH
    LORA_CS = digitalio.DigitalInOut(board.GP1)
    LORA_SCK = board.GP2
    LORA_MOSI = board.GP3
    LORA_MISO = board.GP0
    # Setup Speaker/Buzzer
    AUDIO_GPIO = board.GP4

#------------configure display----------------
displayio.release_displays()

if display_model == "display320x240":
    # Setup Speaker/Buzzer
    AUDIO_GPIO = board.GP0
    #Display configuration
    SPI = busio.SPI(board.GP18, board.GP19)
    display_bus = displayio.FourWire(SPI, command=board.GP16, chip_select=board.GP21)
    display = ST7789(display_bus, rotation=270, width=320, height=240, backlight_pin=board.GP20)
    TERMINAL_HEIGHT=260
     
elif display_model == "display160x80":
    # Setup Speaker/Buzzer
    AUDIO_GPIO = board.GP4
    #Display configuration
    SPI = busio.SPI(board.GP10, board.GP11)
    display_bus = displayio.FourWire(SPI, command=board.GP8, chip_select=board.GP9, reset=board.GP12)
    display = ST7735R(display_bus, width=160, height=80, rotation=90, backlight_pin=board.GP25, rowstart=1, colstart=26, invert=True)
    TERMINAL_HEIGHT=110


SCALE = 1
MAX_LINES = int ((display.height/16)/SCALE)
MAX_CHARS = int ((display.width/8)/SCALE)

display.root_group[0].hidden = False
display.root_group[1].hidden = True # logo
display.root_group[2].hidden = True # status bar
display.root_group.scale = SCALE
supervisor.reset_terminal(int (display.width/SCALE), int (TERMINAL_HEIGHT/SCALE)) #130 #260 #55
display.root_group[0].y = 0



