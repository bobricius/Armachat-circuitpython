import time
import board
import busio
import digitalio
import os
import displayio
import touchio
import microcontroller
from pwmio import PWMOut
from adafruit_st7789 import ST7789
from adafruit_st7735r import ST7735R
import supervisor

#------------configure your device----------------
#device_model="PICOMPUTER"
#device_model="WATCH"
#device_model="WIO"
#device_model="PYPRCAZX"
device_model="PICOPAD"
#device_model="TOUCH"
#GUI=False
#SCALE=1
#LoRa radio configuration
country_code=1
country="US"
#country="EU"
# ---------- Device combination ----------
if device_model=="COMPACT":
    keyboard_model="keys30"
    display_model= "display320x240"
    model_lora = "compact"
    AUDIO_GPIO = board.GP0
elif device_model=="PICOMPUTER":
    keyboard_model="keys36"
    display_model= "display320x240"
    model_lora = "compact"
    AUDIO_GPIO = board.GP0
elif device_model=="WATCH":
    keyboard_model="keys30watch"
    display_model= "display160x80"
    model_lora = "watch"
    AUDIO_GPIO = board.GP4
elif device_model=="WIO":
    keyboard_model="keysWio"
    display_model= "displayWio"
    model_lora = "wio"
    AUDIO_GPIO = board.BUZZER    
elif device_model=="PYPRCAZX":
    keyboard_model="keys49zx"
    display_model= "display320x240zx"
    model_lora = "zx"
    AUDIO_GPIO = board.GP7
elif device_model=="PICOPAD":
    keyboard_model="keys8picopad"
    display_model= "display320x240picopad"
    model_lora = "picopad"
    AUDIO_GPIO = board.GP15
elif device_model=="TOUCH":
    keyboard_model="touch30"
    display_model= "display280x240touch"
    model_lora = "touch"
    AUDIO_GPIO = board.GP22


if country=="EU": #EU
    frequency = 869.525
elif country=="US": #US
    frequency = 906.875
  
signal_bandwidth = 125000
coding_rate = 8
spreading_factor = 12
preamble_length = 32
tx_power=15

# Communicator settings
myName = "Armachat01" #keep exactly 10 chars, it will be stored in NVM
#my address
myAddress = "192.168.1.5"
destination = "192.168.1.5"
maxHops=3
# Encryption password
encryption = True
syncWord = 0x2B
password =   "TopSecretArmachatDeafultPassword"
passwordIv = "0123456789123456"

#Various configuration settings
MAX_INPUT_TEXT = 240
volume = 6
#this is default voltages but by sole lost on diodes and chargers you can addjust
voltageMax=4.2 #fully charged battery
voltageMin=2.5 #empty battery
sleepTime=100 #time in second to reduced brightness
sleepBrightness=0.01 #reduced brightness 0.1 = 10#
lightSleepEnabled=False #if true MCU go to sleep but display radomly flashing
timeInLightSleep=1 # 1=wake every second
ignoreDestination=True # if True you receive all messages / False receive only your messages

#------------configure Radio module connection ----------------
if model_lora == "picopad":
    LORA_CS = digitalio.DigitalInOut(board.GP13)
    LORA_SCK = board.GP10
    LORA_MOSI = board.GP11
    LORA_MISO = board.GP12
    LORA_INT = board.GP28

if model_lora == "compact":
    LORA_CS = digitalio.DigitalInOut(board.GP13)
    #this is alternative LoRa module CS signal
    RXD = digitalio.DigitalInOut(board.GP17)
    LORA_SCK = board.GP10
    LORA_MOSI = board.GP11
    LORA_MISO = board.GP12
    LORA_INT = board.GP28
     
elif model_lora == "watch":
    LORA_CS = digitalio.DigitalInOut(board.GP1)
    LORA_SCK = board.GP2
    LORA_MOSI = board.GP3
    LORA_MISO = board.GP0
    LORA_INT = board.GP28 

elif model_lora == "touch":
    LORA_CS = digitalio.DigitalInOut(board.GP28)
    LORA_SCK = board.GP10
    LORA_MOSI = board.GP11
    LORA_MISO = board.GP12
    LORA_INT = board.GP28 

elif model_lora == "zx":
    LORA_CS = digitalio.DigitalInOut(board.GP13)
    LORA_SCK = board.GP10
    LORA_MOSI = board.GP11
    LORA_MISO = board.GP12
    LORA_INT = board.GP0 

elif model_lora == "wio":
    LORA_CS = digitalio.DigitalInOut(board.CS)
    LORA_SCK = board.SCK
    LORA_MOSI = board.MOSI
    LORA_MISO = board.MISO
    LORA_INT = board.LIGHT 

elif model_lora == "e5":
    print("Lora E5 or NONE")

#------------configure KEYBOARD variants ----------------

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

elif keyboard_model == "keys8picopad":

    keys0 = [
        digitalio.DigitalInOut(x)
        for x in (
                board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7, board.GP8, board.GP9
            )
    ]


elif keyboard_model == "keys49zx":
    rows = [
        digitalio.DigitalInOut(x)
        for x in (board.GP8, board.GP9, board.GP14, board.GP15, board.GP16, board.GP17, board.GP18)
    ]
    cols = [
        digitalio.DigitalInOut(x)
        for x in (board.GP19, board.GP20, board.GP21, board.GP22, board.GP26, board.GP27, board.GP28)
    ]
    keys1 = (
        ("ent", "lt", "up", "rt", "dn", "alt", "."),
        ("1", "2", "3", "4", "5", "6", "7"),
        ("8", "9", "0", "q", "w", "e", "r"),
        ("t", "y", "u", "i", "o", "p", "a"),
        ("s", "d", "f", "g", "h", "j", "k"),
        ("l", "bsp", "z", "x", "c", "v", "b"),
        ("n", "m", " ", "*", "/", "-", "+"),
    )

    keys2 = (
        ("tab", "lt", "up", "dn", "rt", "alt", "ss"),
        ("!", "@", "#", "$", "%", "&", "'"),
        ("(", ")", "_", "Q", "W", "E", "<"),
        (">", "[", "]", "I", ";", '"', "~"),
        ("|", "\\", "{", "}", "^", "-", "+"),
        ("=", "ent", ":", "X", "?", "/", "B"),
        (",", ".", " ", "mn", "rl", "pr", "nx"),
    )

    keys3 = (
        ("tab", "lt", "up", "dn", "rt", "alt", "ss"),
        ("1", "2", "3", "4", "5", "6", "7"),
        ("8", "9", "0", "Q", "W", "E", "R"),
        ("T", "Y", "U", "I", "O", "P", "A"),
        ("S", "D", "F", "G", "H", "J", "K"),
        ("L", "ent", "Z", "X", "C", "V", "B"),
        ("N", "M", " ", "mn", "rl", "pr", "nx"),
    )



elif keyboard_model == "keys30watch":
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

elif keyboard_model == "touch30":
    touch9c = touchio.TouchIn(board.GP3)
    touch8c = touchio.TouchIn(board.GP4)
    touch7c = touchio.TouchIn(board.GP5)
    touch6c = touchio.TouchIn(board.GP6)
    touch5c = touchio.TouchIn(board.GP7)
    touch4c = touchio.TouchIn(board.GP8)
    touch3c = touchio.TouchIn(board.GP9)
    touch2c = touchio.TouchIn(board.GP13)
    touch1c = touchio.TouchIn(board.GP14)
    touch0c = touchio.TouchIn(board.GP15)
    touch0r = touchio.TouchIn(board.GP2)
    touch1r = touchio.TouchIn(board.GP1)
    touch2r = touchio.TouchIn(board.GP0)

    keys1 = (
        ("q", "w", "e", "r", "t","y", "u", "i", "o", "p"),
        ("a", "s", "d", "f", "g","h", "j", "k", "l", "bsp"),
        ("alt", "z", "x", "c", "v","b", "n", "m", " ", "ent"),
    )
    keys2 = (
        ("1", "2", "3", "4", "5","6", "7", "8", "9", "0"),
        ("!", "@", "#", "$", "%","+", "&", "*", "-", "lt"),
        ("alt", "(", ")", "?", "/","""""", ";", ":", ".", "rt"),
    )
    keys3 = (
        ("Q", "W", "E", "R", "T","Y", "U", "I", "O", "P"),
        ("A", "S", "D", "F", "G","H", "J", "K", "L", "up"),
        ("alt", "Z", "X", "C", "V","B", "N", "M", ",", "dn"),
    )
    
elif keyboard_model == "keysWio":
    cols = [
        digitalio.DigitalInOut(x)
        for x in (board.I2S_BCLK, board.DAC0, board.D4, board.D5, board.DAC1)
    ]
    rows = [
        digitalio.DigitalInOut(x)
        for x in (board.I2S_SDOUT, board.I2S_SDIN, board.D8, board.D7, board.I2S_LRCLK, board.D6)
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

#------------configure display----------------

if display_model == "display320x240":
    displayio.release_displays()
    SPI = busio.SPI(board.GP18, board.GP19)
    display_bus = displayio.FourWire(SPI, command=board.GP16, chip_select=board.GP21)
    display = ST7789(display_bus, rotation=270, width=320, height=240, backlight_pin=board.GP20, backlight_pwm_frequency=500)
    MAX_CHARS = 26

elif display_model == "display320x240zx":
    displayio.release_displays()
    SPI = busio.SPI(board.GP2, board.GP3)
    display_bus = displayio.FourWire(SPI, command=board.GP6, chip_select=board.GP5)
    display = ST7789(display_bus, rotation=270, width=320, height=240, backlight_pin=board.GP4, backlight_pwm_frequency=500)
    MAX_CHARS = 26

elif display_model == "display320x240picopad":
    displayio.release_displays()
    SPI = busio.SPI(board.GP18, board.GP19)
    display_bus = displayio.FourWire(SPI, command=board.GP17, chip_select=board.GP21, reset=board.GP20)
    display = ST7789(display_bus, rotation=270, width=320, height=240, backlight_pin=board.GP16, backlight_pwm_frequency=500)
    MAX_CHARS = 26

elif display_model == "display280x240":
    displayio.release_displays()
    SPI = busio.SPI(board.GP18, board.GP19)
    display_bus = displayio.FourWire(SPI, command=board.GP16, chip_select=board.GP21)
    display = ST7789(display_bus, rotation=270, width=280, height=240, rowstart=20, backlight_pin=board.GP20)
    MAX_CHARS = 23

elif display_model == "display280x240touch":
    displayio.release_displays()
    SPI = busio.SPI(board.GP18, board.GP19)
    display_bus = displayio.FourWire(SPI, command=board.GP26, chip_select=board.GP21)
    display = ST7789(display_bus, rotation=270, width=280, height=240, rowstart=20, backlight_pin=board.GP20)
    MAX_CHARS = 23

elif display_model == "display160x80":
    displayio.release_displays()
    SPI = busio.SPI(board.GP10, board.GP11)
    display_bus = displayio.FourWire(SPI, command=board.GP8, chip_select=board.GP9, reset=board.GP12)
    display = ST7735R(display_bus, width=160, height=80, rotation=90, backlight_pin=board.GP25, rowstart=1, colstart=26, invert=True)
    MAX_CHARS = 23
    
elif display_model == "display160x80emul":
    displayio.release_displays()
    SPI = busio.SPI(board.GP18, board.GP19)
    display_bus = displayio.FourWire(SPI, command=board.GP16, chip_select=board.GP21)
    display = ST7789(display_bus, width=160, height=80, rotation=270, backlight_pin=board.GP20, rowstart=0, colstart=0)
    MAX_CHARS = 23

elif display_model == "displayWio":
    display = board.DISPLAY
    MAX_CHARS = 26
    
print (".CONFIG DONE")