debug = False
import time
import alarm
import sys,supervisor
import usb_cdc
import board
import busio
import terminalio
import displayio
import analogio
import gc
import os
import aesio
from binascii import hexlify
import microcontroller
from adafruit_display_text import label, wrap_text_to_lines, bitmap_label
from adafruit_display_shapes.rect import Rect
#from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.roundrect import RoundRect
#from adafruit_display_shapes.triangle import Triangle
#from adafruit_display_shapes.line import Line
#from adafruit_display_shapes.polygon import Polygon
from adafruit_simple_text_display import SimpleTextDisplay
from pwmio import PWMOut
from adafruit_bitmap_font import bitmap_font
from picomputer import *
import digitalio
import random

GUI = True
line = ["#hello world", "a=2", "b=7","c=1", "print(a+b+c)", "for i in range(a, b):", " print('index:'+str(i))"," beep()", "", "", ""]

########################################################################################
######### MOST IMPORTANT PART - Like main loop, reading keyboard a receiving messages
########################################################################################
def editor(text):
    cursor = 0
    layout = 0
    editLine = 0
    editText = line[0]
    editMode = "#"
    layoutName = "a"
    receivedMessage=""


    EditorScreen[1].text = line[0]
    EditorScreen[2].text = line[1]
    EditorScreen[3].text = line[2]    
    EditorScreen[4].text = line[3]
    EditorScreen[5].text = line[4]
    EditorScreen[6].text = line[5]
    EditorScreen[7].text = line[6]    
    EditorScreen[8].text = line[7]
    EditorScreen[9].text = line[8]
    EditorScreen[10].text = line[9]  

    displayRefresh=True
    sleepStart_time = time.monotonic()  # fraction seconds uptime
    EditorScreen[0].text="PYCOmputer"

    while True:
#         if time.monotonic() - sleepStart_time > sleepTime:  # every 2 seconds
#             display.brightness = sleepBrightness
#             if lightSleepEnabled==True:
#                 goToSleep()
      
        
        keys=getKey(layout)
          
        if keys:
            sleepStart_time = time.monotonic()  # fraction seconds uptime
            display.brightness = 1
            if keys == "alt":
                layout = layout + 1
                ring()
                displayRefresh=True
                if layout == 3:
                    layout = 0
                keys = ""
                

            if keys == "ent" and line == "":
                line[editLine]=editText
                EditorScreen[editLine+1].text = editText
                if editLine<9 :editLine=editLine+1

                editText=line[editLine]
                cursor = 0
                keys = ""
                displayRefresh=True

            if keys == "bsp":
                if cursor > 0:
                    editText = (editText[0 : cursor - 1]) + (editText[cursor:])
                    cursor = cursor - 1
                    beep()
                    displayRefresh=True
                while getKey(0):
                    pass
                keys = ""
            if keys == "lt":
                if cursor > 0:
                    cursor = cursor - 1
                keys = ""
                displayRefresh=True
            if keys == "rt":
                if cursor < len(editText):
                    cursor = cursor + 1
                keys = ""
                displayRefresh=True
            if keys == "up":
                line[editLine]=editText
                EditorScreen[editLine+1].text = editText
                if editLine>0 :editLine=editLine-1
                editText=line[editLine]
                cursor = 0
                keys = ""
                displayRefresh=True
            if keys == "dn":
                line[editLine]=editText
                EditorScreen[editLine+1].text = editText
                if editLine<9 :editLine=editLine+1

                editText=line[editLine]
                cursor = 0
                keys = ""
                displayRefresh=True


            if keys == "tab":
                ring()
                execText = ""
                for oneLine in line:
                    if oneLine.strip() != "":
                        execText += oneLine+"\n"
                return execText
            if keys != "":
                if len(editText) < MAX_INPUT_TEXT:
                    editText = (editText[0:cursor]) + keys + (editText[cursor:])
                    cursor = cursor + 1
                    layout = 0
                    beep()
                    displayRefresh=True
                    while getKey(0):
                        pass
            
        if layout == 0:
            layoutName = "_"
        elif layout == 1:
            layoutName = "|"
        elif layout == 2:
            layoutName = "-"
        line[editLine] = editText  # (editText[0:cursor])+"_"+(editText[cursor:])
        textInput = (editText[0:cursor]) + layoutName + (editText[cursor:]) # line[editLine]
        textLen = len(editText)
        maxLine=MAX_CHARS-3
        if textLen > maxLine and cursor > maxLine:
            textInput = (textInput[cursor-maxLine:cursor+1])
        textInput = (textInput[:maxLine+1])
        
        if displayRefresh==True:
            displayRefresh=False
            EditorScreen[0].text="PYCOmputer - "+str(editLine)+":"+str(cursor)
            EditorScreen[editLine+1].text =textInput
            EditorScreen.show()
            #text_edit.text=editMode+textInput #layoutName+editMode+
            #text_layout.text=str(textLen)

def goToSleep():
        display.brightness = 0.001
        time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + timeInLightSleep)
        pin_alarm = alarm.pin.PinAlarm(LORA_INT, value=True, pull=True)
        #print("sleep")
        alarm.light_sleep_until_alarms(time_alarm, pin_alarm)
        #display.brightness = 0.1
        #print("wake")


def debugPrint (msg):
    if debug:
        print ("----["+msg+"]")
        



def clearScreen():
    print("...")

def bool2onoff(bvar):
    if bvar == True:
        onoff = "On"
    else:
        onoff = "Off"
    return onoff



        



def filesystemInfo():
    fs_stat = os.statvfs('/')
    text = "Filesystem:\n"
    text = text +"Disk size:"+str(fs_stat[0] * fs_stat[2] / 1024 )+" KB\n"
    text = text + "Free space:"+str(fs_stat[0] * fs_stat[3] / 1024 )+" KB\n"
    if supervisor.runtime.usb_connected:
        text = text + "USB connected\n"
    ring()
    return text

def powerInfo():
    text = "Battery:\n"   
    text = text +"VSYS = {:5.2f} V\n".format(((VSYS_voltage.value * 3.3) / 65536) * 3)
    if VBUS_status.value :
        text = text +"USB powered\n"
    else:
        text = text +"No USB power\n"   
    ring()
    return text

def batteryInfo():
    voltage =((VSYS_voltage.value * 3.3) / 65536) * 3
    capacity= int(min(max((0 + ((voltage - voltageMin) * (100 - 0) / (voltageMax - voltageMin))), 0), 100))
    return capacity
# ----------------------FUNCTIONS---------------------------

# with open('x.txt', 'w') as f:
#    f.write("Hello world!\r\n")
#    f.close()

############################################################################
######### SETUP - Program start
############################################################################
board_type = os.uname().machine
if 'Pico' in board_type:
    VSYS_voltage = analogio.AnalogIn(board.VOLTAGE_MONITOR)
    VBUS_status = digitalio.DigitalInOut(board.VBUS_SENSE)  # defaults to input
    VBUS_status.pull = digitalio.Pull.UP  # turn on internal pull-up resistor
    SMPSmode = digitalio.DigitalInOut(board.SMPS_MODE)
    SMPSmode.direction = digitalio.Direction.OUTPUT
    SMPSmode.value = True
    #LED = digitalio.DigitalInOut(board.GP25)
    #LED.direction = digitalio.Direction.OUTPUT 

############################################################################
######### Start simple text
############################################################################
print("Starting GUI...")

font_file = "fonts/gomme-20.pcf" 
font = bitmap_font.load_font(font_file)
EditorScreen = SimpleTextDisplay(display=display,font=font,text_scale=1,
                                 colors=(SimpleTextDisplay.YELLOW, SimpleTextDisplay.WHITE,SimpleTextDisplay.WHITE,
                                         SimpleTextDisplay.WHITE,SimpleTextDisplay.WHITE, SimpleTextDisplay.WHITE,
                                         SimpleTextDisplay.WHITE,SimpleTextDisplay.WHITE,SimpleTextDisplay.WHITE,SimpleTextDisplay.WHITE,SimpleTextDisplay.WHITE,SimpleTextDisplay.GREEN))

EditorScreen[0].text = "PYCOmputer"
EditorScreen[1].text = "1"
EditorScreen[2].text = "2"
EditorScreen[3].text = "3"
EditorScreen[4].text = "4"
EditorScreen[5].text = "5"
EditorScreen[6].text = "6"
EditorScreen[7].text = "7"
EditorScreen[8].text = "8"
EditorScreen[9].text = "9"
EditorScreen[10].text = "10"
EditorScreen[11].text = "[ESC] - RUN PROGRAM"

EditorScreen.show()
############################################################################
######### Start loop
############################################################################

#supervisor.set_next_code_file("ArmachatGUI.py")

#configuration load/save
# microcontroller.nvm[0:3] = b"000"
# print (microcontroller.nvm[0])

# Define pins connected to the chip.

print ("Editor ready ...")


############################################################################
######### MAIN LOOP
############################################################################


while True:
    ### most important part, editor checking keyboard and receiving messages
    text = editor(text="")
    EditorScreen.show_terminal()
    print ("... Program start ...")
    print (text)
    print ("... Program response ...")
    try:
        exec(text)
    except Exception as err:
        print(err)

    ring()
    keys = getKey(0)
    while not keys:
        keys = getKey(0)
