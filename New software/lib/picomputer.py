from pwmio import PWMOut
from config import *
import digitalio
import adafruit_matrixkeypad

def beep():
    audioPin = PWMOut(AUDIO_GPIO, duty_cycle=0, frequency=440, variable_frequency=True)
    audioPin.frequency = 5000
    audioPin.duty_cycle = 1000 * (volume)
    time.sleep(0.002)
    audioPin.duty_cycle = 0
    audioPin.deinit()
    
def ring():
    audioPin = PWMOut(AUDIO_GPIO, duty_cycle=0, frequency=440, variable_frequency=True)
    audioPin.frequency = 2000
    audioPin.duty_cycle = 1000 * (volume)
    time.sleep(0.1)
    audioPin.frequency = 3000
    audioPin.duty_cycle = 1000 * (volume)
    time.sleep(0.1)
    audioPin.frequency = 6000
    audioPin.duty_cycle = 1000 * (volume)
    time.sleep(0.1)
    audioPin.duty_cycle = 0
    audioPin.deinit()

def getKey(layout):
    if layout == 0:
        keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys1)
        #layoutName = "a"
    elif layout == 1:
        keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys2)
        #layoutName = "1"
    elif layout == 2:
        keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys3)
        #layoutName = "A"
    keys = keypad.pressed_keys

    return keys

def get_VSYSvoltage():
    VSYSin = ((VSYS_voltage.value * 3.3) / 65536) * 3
    return VSYSin
