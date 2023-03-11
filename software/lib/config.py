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
#GUI=False
#SCALE=1
#------------configure keyboard----------------
keyboard_model="keys36"
#keyboard_model="keys30"
#keyboard_model="touch30"
#keyboard_model="keysWio"
#keyboard_model="keys30watch"
#------------configure display----------------
display_model= "display320x240"
#display_model= "display280x240touch"
#display_model= "displayWio"
#display_model= "display280x240"
#display_model= "display160x80"
#display_model= "display160x80emul" #emulated display in window
#------------configure Radio module connection ----------------
model_lora = "compact"
#model_lora = "watch"
#model_lora = "touch"
#model_lora = "e5"

#LoRa radio configuration
country_code=1
country="EU"

if country=="EU": #EU
    frequency = 869.525
elif country=="US": #US
    frequency = 906.875


  
signal_bandwidth = 125000
coding_rate = 8
spreading_factor = 12
preamble_length = 32
tx_power=15

# Communicator
myName = "bobricius"
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
sleepTime=100 #time in second to sleep display
sleepBrightness=0.01 #reduced brightness 0.1 = 10#
lightSleepEnabled=False #if true MCU go to sleep but display radomly flashing
timeInLightSleep=1 # 1=wake every second
ignoreDestination=True # if True you receive all messages/ False receive only your messages

#------------configure Radio module connection ----------------
#model_lora = "compact"
#model_lora = "watch"

if model_lora == "compact":
    #Lora HW configuration MAX
    LORA_CS = digitalio.DigitalInOut(board.GP13)
    #this is alternative LoRa module CS signal
    RXD = digitalio.DigitalInOut(board.GP17)
    LORA_SCK = board.GP10
    LORA_MOSI = board.GP11
    LORA_MISO = board.GP12
    LORA_INT = board.GP28
     
elif model_lora == "watch":
    #Lora HW configuration WATCH
    LORA_CS = digitalio.DigitalInOut(board.GP1)
    LORA_SCK = board.GP2
    LORA_MOSI = board.GP3
    LORA_MISO = board.GP0
    LORA_INT = board.GP28 

elif model_lora == "touch":
    #Lora HW configuration WATCH
    LORA_CS = digitalio.DigitalInOut(board.GP28)
    LORA_SCK = board.GP10
    LORA_MOSI = board.GP11
    LORA_MISO = board.GP12
    LORA_INT = board.GP28 

elif model_lora == "e5":
    print("Lora E5")



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

elif keyboard_model == "touch30":
    # Setup Keyboard
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
    print("Wio keyboard")
    
    
    
# ----------         End of Keyboard Settings          ----------

#------------configure display----------------
#displayio.release_displays()

if display_model == "display320x240":
    # Setup Speaker/Buzzer
    AUDIO_GPIO = board.GP0
    #Display configuration
    displayio.release_displays()
    SPI = busio.SPI(board.GP18, board.GP19)
    display_bus = displayio.FourWire(SPI, command=board.GP16, chip_select=board.GP21)
    display = ST7789(display_bus, rotation=270, width=320, height=240, backlight_pin=board.GP20, backlight_pwm_frequency=500)
    TERMINAL_HEIGHT=130
    MAX_CHARS = 26
    
elif display_model == "displayWio":
    display = board.DISPLAY
    AUDIO_GPIO = board.BUZZER
    TERMINAL_HEIGHT=280
    MAX_CHARS = 26


elif display_model == "display280x240":
    displayio.release_displays()
    # Setup Speaker/Buzzer
    AUDIO_GPIO = board.GP22
    #Display configuration
    displayio.release_displays()
    SPI = busio.SPI(board.GP18, board.GP19)
    display_bus = displayio.FourWire(SPI, command=board.GP16, chip_select=board.GP21)
    display = ST7789(display_bus, rotation=270, width=280, height=240, rowstart=20, backlight_pin=board.GP20)
    TERMINAL_HEIGHT=280
    MAX_CHARS = 23

elif display_model == "display280x240touch":
    displayio.release_displays()
    # Setup Speaker/Buzzer
    AUDIO_GPIO = board.GP22
    SPI = busio.SPI(board.GP18, board.GP19)
    display_bus = displayio.FourWire(SPI, command=board.GP26, chip_select=board.GP21)
    display = ST7789(display_bus, rotation=270, width=280, height=240, rowstart=20, backlight_pin=board.GP20)
    TERMINAL_HEIGHT=280
    MAX_CHARS = 23

elif display_model == "display160x80":
    # Setup Speaker/Buzzer
    AUDIO_GPIO = board.GP4
    #Display configuration
    displayio.release_displays()
    SPI = busio.SPI(board.GP10, board.GP11)
    display_bus = displayio.FourWire(SPI, command=board.GP8, chip_select=board.GP9, reset=board.GP12)
    display = ST7735R(display_bus, width=160, height=80, rotation=90, backlight_pin=board.GP25, rowstart=1, colstart=26, invert=True)
    TERMINAL_HEIGHT=95
    display.root_group[0].hidden = False
    display.root_group[1].hidden = False # logo
    display.root_group[2].hidden = False # status bar
    #display.root_group.scale = SCALE
    supervisor.reset_terminal(display.width,TERMINAL_HEIGHT) #130 #260 #55
    display.root_group[0].y = 10
    MAX_CHARS = 23
    
elif display_model == "display160x80emul":
    # Setup Speaker/Buzzer
    # Setup Speaker/Buzzer
    AUDIO_GPIO = board.GP0
    #Display configuration
    displayio.release_displays()
    AUDIO_GPIO = board.GP0
    SPI = busio.SPI(board.GP18, board.GP19)
    display_bus = displayio.FourWire(SPI, command=board.GP16, chip_select=board.GP21)
    display = ST7789(display_bus, width=160, height=80, rotation=270, backlight_pin=board.GP20, rowstart=0, colstart=0)
    TERMINAL_HEIGHT=95
    display.root_group[0].hidden = False
    display.root_group[1].hidden = False # logo
    display.root_group[2].hidden = False # status bar
    #display.root_group.scale = SCALE
    supervisor.reset_terminal(display.width,TERMINAL_HEIGHT) #130 #260 #55
    display.root_group[0].y = 10
    MAX_CHARS = 23

# if SCALE==2:
#     display.root_group.scale = SCALE
#     supervisor.reset_terminal(display.width,TERMINAL_HEIGHT)
