debug = False
import time
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
import math
from binascii import hexlify
import microcontroller
from adafruit_display_text import label, wrap_text_to_lines
from adafruit_display_shapes.rect import Rect
#from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.roundrect import RoundRect
#from adafruit_display_shapes.triangle import Triangle
#from adafruit_display_shapes.line import Line
#from adafruit_display_shapes.polygon import Polygon
from pwmio import PWMOut
from adafruit_bitmap_font import bitmap_font
from picomputer import *
from math import *
import digitalio
import random

messages = ["0.0.0.0|0.0.0.0|0.0.0.0|0.0.0.0|x|0|0|0| MESSAGE MEMORY:"]
msgCounter = 0
GUI=True
########################################################################################
######### MOST IMPORTANT PART - Like main loop, reading keyboard a receiving messages
########################################################################################
def editor(text):
    cursor = 0
    layout = 0
    editLine = 0
    editText = text
    editMode = "#"
    layoutName = "a"
    receivedMessage=""
    line = ""
    displayRefresh=True
    #print ("> \r", end='')  #
    while True:
        
        
        keys=getKey(layout)         
        if keys:
            if keys == "alt":
                layout = layout + 1
                ring()
                displayRefresh=True
                if layout == 3:
                    layout = 0
                keys = ""
                
            if keys == "bsp" and line == "":
                text = "~bsp"
                return text
            if keys == "ent" and line == "":
                text = "~ent"
                return text
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
            
            if keys == "ent":
                beep()
                text = line
                return text
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
        line = editText  # (editText[0:cursor])+"_"+(editText[cursor:])
        textInput = (editText[0:cursor]) + layoutName + (editText[cursor:]) # line[editLine]
        textLen = len(editText)
        maxLine=MAX_CHARS-3
        if textLen > maxLine and cursor > maxLine:
            textInput = (textInput[cursor-maxLine:cursor+1])
        textInput = (textInput[:maxLine+1])
        
        if displayRefresh==True:
            if GUI==True:
                cmdMode=len(editText)
                editMode=""
                text_edit.text=editMode+textInput #layoutName+editMode+
                #text_layout.text=str(textLen)
                
            else:
                print("\033]0;>>"+textInput+"\033\\",end="")
                #if display_model== "display280x240" or display_model== "display280x240touch":
                #    layoutName="     "+layoutName  #move text away from rounded corner
                #print ((editMode)+textInput+" \r", end='')
                #print("\033]0;"+textInput+"\033\\")
            #if displayRefresh==True:
                #print("\033]0;"+textInput+"\033\\")
                #display.refresh()
                displayRefresh=False





### AI CODE
lines = ['Line 1', 'Line 2', 'Line 3']
num_lines = 100
displayed_lines = 6

def add_line(new_line):
    global lines
    lines.append(new_line)
    if len(lines) > num_lines:
        lines = lines[-num_lines:]
        
def display_lines(start_line):
    if start_line >= len(lines):
        print("Invalid start line. The number of lines is", len(lines))
        return
    lines_to_display = []
    for line in lines[start_line:]:
        lines_to_display += line.split('\n')
    for line in lines_to_display[-displayed_lines:]:
        print(line)


### END AICODE
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


def readCardKB():
    if M5CardKB==True:           
        ESC = chr(27)
        NUL = '\x00'
        CR = "\r"
        LF = "\n"
        c = ''
        b = bytearray(1)
        i2c.readfrom_into(cardkb, b)
        try:
            c = b.decode()
        except:
            c = NUL
           
        if c != NUL:
            if b[0] == 0x08:
                c = "bsp"
            if b[0] == 0x0D:
                c = "ent"
            if b[0] == 0xB4:
                c = "lt"
            if b[0] == 0xB7:
                c = "rt"
            keys= c
            print(c)



def listMemory(details=True):
    for i, msg in enumerate(messages):
      # Split the message into a list of values using the "|" delimiter
        values = msg.split("|")
        msgStatus=values[4]
        if msgStatus=="R":
          msgStatus="<-"
        elif msgStatus=="S":
          msgStatus="? "
        elif msgStatus=="D":
          msgStatus="->"
          
        addFromTo = ">".join(values[0:2])
        if details==True:
            print(str(i)+"# "+addFromTo)
            print(msgStatus+values[-1]) #text
            print("RSSI:"+values[5]+" SNR:"+values[6] )
        else:
            print(str(i)+"# "+msgStatus+values[-1]) #text


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

############################################################################
######### Resize terminal
############################################################################
if GUI==True:
    # Create a Group
    mygroup = displayio.Group()

    print("Starting GUI...")

    display.show(None)
    splash = display.root_group # this gets the current root_group, the REPL

    # Note: You must "display.show" your own group before adding the splash to your own group.
    # Reason: When displaying the normal REPL (for example with display.show(None), the splash
    # group is already in a group that is displayed.  To remove the splash from the displayed group,
    # you first have to display.show some other group, doing that will remove the splash from its group
    # and allow you to append it to your own group.	
    display.show(mygroup)

    # resize the supervisor.splash group pixel dimensions, make it half the display height.
    supervisor.reset_terminal(display.width, 60+24) #+12

    # relocate the supervisor.splash group on the display, moving it half-way down the display
    splash.y=180-12 # -12
    print("Resize and move terminal ....")

    # append the supervisor.splash group to the displayed group.
    mygroup.append(splash)

    font_file = "fonts/neep-24.pcf"
    font = bitmap_font.load_font(font_file)
    terminal_font = terminalio.FONT
    
    window_roundrect = RoundRect(0, 0, display.width, 147, 4, fill=0xFFFFFF, outline=0xF0F0F0, stroke=2)
    edit_roundrect = RoundRect(0, 150, display.width, 30, 4, fill=0xFFFFFF, outline=0xF0F0F0, stroke=2)


    text_window = label.Label(font, line_spacing=1, text="PyPrCa", color=0, x=1, y=12)
    text_edit = label.Label(font, line_spacing=1, text="TEXT", color=0, x=2, y=162)


    mygroup.append(window_roundrect)

    mygroup.append(edit_roundrect)

    mygroup.append(text_window)
    mygroup.append(text_edit)

############################################################################
######### Start loop
############################################################################



if keyboard_model=="keysWio":
    M5CardKB=True
    #i2c for CardKB 
    i2c = busio.I2C(board.SCL, board.SDA)
    while not i2c.try_lock():
        pass
    try: 
        cardkb = i2c.scan()[0]  # should return 95
        if cardkb != 95:
            print("!!! Check I2C config: " + str(i2c))
            print("!!! CardKB not found. I2C device", cardkb,
                  "found instead.")
            M5CardKB=False
        else :
            print("CardKB detected Great")
            print()    
    except:
        M5CardKB=False
        print("No CardKB detected !")
        print()

if supervisor.runtime.usb_connected:
    print ("..... USB connected")
############################################################################
######### MAIN LOOP
############################################################################
print("Starting Calculator...")
lastMessage =0
message = ""
messageDetails=False

while True:
    sleepStart_time = time.monotonic()  # fraction seconds uptime
    ### most important part, editor checking keyboard and receiving messages
    #display.auto_refresh = False
    text =editor(text=message)
    #display.refresh()
    #display.auto_refresh = True
    if text=="~bsp":
        lastMessage = max(0, lastMessage - 1)
        #displayMessage(lastMessage,messageDetails)
        continue
    if text=="~ent":
        lastMessage = min(len(messages) - 1, lastMessage + 1)
        #displayMessage(lastMessage,messageDetails)
        continue

    if len(text) == 1:
        if text == "h":
            #[G]ping [P]Profile [F]Frequency 
            cmdInfo = "HELP: [E]edit [M]Memory\n[L]List [R]Radio\n[C]crypto [D]Debug\n[G]ping"
        elif text == "c":
            encryption = not encryption
            cmdInfo = "Enctryption:"+bool2onoff(encryption)
        elif text == "e":
            cmdInfo = "Editing message:"+str(lastMessage)
            message = displayMessage(lastMessage,False)
        elif text == "d":
            debug = not debug
            cmdInfo = "Debug messages:"+bool2onoff(debug)
        elif text == "m":
            cmdInfo = memoryInfo()
        elif text == "l":
            messageDetails = not messageDetails
            cmdInfo = "Message Details:"+bool2onoff(messageDetails)
        elif text == "r":
            cmdInfo = radioInfo()
        elif text == "g":
            pingBeacon()
            cmdInfo = "Beacon finished"           
            
        else:
            cmdInfo = "Try for [H] help"

    # Print the template
        #cmdInfo = "\n".join(wrap_text_to_lines(cmdInfo, MAX_CHARS))
        #print(cmdInfo)
        if GUI==True:
            text_window.text=cmdInfo
        ring()
        ring()
    else:
        print ("->"+text)
        try:
            res=str(eval(text))
            exec("a=3")
        except Exception as err:
            print(err)
            text_window.text=str(err)
        
        text = "\n".join(wrap_text_to_lines(res, MAX_CHARS))
        print (text)
        if GUI==True:
            text_window.text=text
        message = ""
        lastMessage=len(messages)-1