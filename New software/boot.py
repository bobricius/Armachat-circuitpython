import time
import board
import busio
import gc
import displayio
import digitalio
import microcontroller
import storage

#from config import *
from picomputer import *


VBUS_status = digitalio.DigitalInOut(board.VBUS_SENSE)  # defaults to input
VBUS_status.pull = digitalio.Pull.UP  # turn on internal pull-up resistor

#display is configured in /lib/config.py

if VBUS_status.value:
    print("USB powered")
else:
    print("No USB power")
writemode = True

print ("Keyboard:"+keyboard_model)
print ("Display:"+display_model)
print ("LoRa:"+model_lora)
#pnt20"12345678901234567890")
print("[ESC]-SAFE [ALT]-RW")

LOOPCOUNT = 15
for x in range(LOOPCOUNT):
    s = "["
    for i in range(0, LOOPCOUNT):
        if (LOOPCOUNT - 1) - i > x:
            s = s + "-"
        else:
            s = s + " "
    if x == LOOPCOUNT - 1:
        print(s + "]\n")
    else:
        print(s + "]\r", end='')

    time.sleep(0.05)
    keys =getKey(0)

    if not keys:
        continue
    if keys[0] == "bsp":
        print("SAFE MODE DETECTED.")
        microcontroller.on_next_reset(microcontroller.RunMode.SAFE_MODE)
        microcontroller.reset()
    if keys[0] == "alt":
        print("Write mode enabled.")
        writemode = False

# RENAME DRIVE
new_name = "PICOmputer"

storage.remount("/", readonly=False)
m = storage.getmount("/")
m.label = new_name
storage.remount("/", readonly=writemode)
print("Free memory:")
print(gc.mem_free())
#pnt20"12345678901234567890")
print("Loading DOS ...")
