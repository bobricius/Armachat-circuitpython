from pwmio import PWMOut
from config import *
import digitalio
import busio
from digitalio import DigitalInOut, Direction, Pull
import adafruit_matrixkeypad

def beep():
    audioPin = PWMOut(AUDIO_GPIO, duty_cycle=0, frequency=440, variable_frequency=True)
    audioPin.frequency = 4000
    audioPin.duty_cycle = 10000 * (volume)
    time.sleep(0.01)
    audioPin.duty_cycle = 0
    audioPin.deinit()
    
def ring():
    audioPin = PWMOut(AUDIO_GPIO, duty_cycle=0, frequency=440, variable_frequency=True)
    audioPin.frequency = 4000
    audioPin.duty_cycle = 1000 * (volume)
    time.sleep(0.05)
    audioPin.duty_cycle = 0
    audioPin.deinit()
    time.sleep(0.2)
    audioPin = PWMOut(AUDIO_GPIO, duty_cycle=0, frequency=440, variable_frequency=True)
    audioPin.frequency = 8000
    audioPin.duty_cycle = 1000 * (volume)
    time.sleep(0.05)
    audioPin.duty_cycle = 0    
    audioPin.deinit()

def getKey(layout):

    keys = ""
    if keyboard_model == "touch30":
        touch_rows = [touch0r.value,touch1r.value,touch2r.value]
        touch_cols = [touch0c.value,touch1c.value,touch2c.value,
                      touch3c.value,touch4c.value,touch5c.value,
                      touch6c.value,touch7c.value,touch8c.value,
                      touch9c.value]
        r=0
        for tr in touch_rows:
            r=r+1
            if tr:
                c=0
                for tc in touch_cols:
                    c=c+1
                    if tc:
                        #print (r,c)
                        if layout == 0:
                            return (keys1[r-1][c-1])
                        elif layout == 1:
                            return (keys2[r-1][c-1])
                        elif layout == 2:
                            return (keys3[r-1][c-1])
        return keys
                        
    elif keyboard_model=="keys36" or keyboard_model=="keys30" or keyboard_model=="keys30watch" or keyboard_model=="keys49zx" or keyboard_model=="keysWio":
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
        if keys:
            keys = keys[0]
            
        
    elif keyboard_model=="keys8picopad":
        keys=""
        keys0[0].switch_to_input(Pull.UP) #right
        keys0[1].switch_to_input(Pull.UP) #left       
        keys0[2].switch_to_input(Pull.UP) #up
        keys0[3].switch_to_input(Pull.UP) #down
        keys0[4].switch_to_input(Pull.UP) #B
        keys0[5].switch_to_input(Pull.UP) #A       
        keys0[6].switch_to_input(Pull.UP) #Y
        keys0[7].switch_to_input(Pull.UP) #X

        if keys0[0].value is False:
            keys="rt"
        if keys0[1].value is False:
            keys="lt"
        if keys0[2].value is False:
            keys="up"
        if keys0[3].value is False:
            keys="dn"
        if keys0[4].value is False:
            keys="ent"
        if keys0[5].value is False:
            keys="bsp"
        if keys0[6].value is False:
            keys="pgdown"
        if keys0[7].value is False:
            keys="pgup"
    return keys

def get_VSYSvoltage():
    VSYSin = ((VSYS_voltage.value * 3.3) / 65536) * 3
    return VSYSin
