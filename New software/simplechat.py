import time
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
#from adafruit_simple_text_display import SimpleTextDisplay
#import adafruit_matrixkeypad
#from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label, wrap_text_to_lines
from pwmio import PWMOut
#from adafruit_display_text import label
#from adafruit_st7789 import ST7789

from picomputer import *
import digitalio
import random
import armachat_lora

messages = ["1|2|3|4|5|6|7|8|Memory|a2|a3|a4|a5|a6|a7|a8"]
msgCounter = 0x00
#message = None


def changeMessageStatus(msgID="", old="", new=""):
    allMsg = len(messages)
    c = 0
    #log.logValue("changeMessageStatus", "msgID", msgID)
    for i in range(allMsg):
        if messages[i].count(msgID) > 0:
            messages[i] = messages[i].replace(old, new)
            c = c + 1
    return c


def clearScreen():
    print("...")


def countMessages(msgStat=""):
    if msgStat is None:
        return 0
    allMsg = len(messages)
    c = 0
    for i in range(allMsg):
        if messages[i].count(msgStat) > 0:
            c = c + 1
    return c


def editor(text):
    cursor = 0
    layout = 0
    editLine = 0
    editText = text
    editMode = "#"
    layoutName = "a"
    receivedMessage=""
    line = ""
    print (">> \r", end='')  #
    while True:
        receivedMessage = receiveMessage()
        if receivedMessage is not None:
            #message = "\n".join(wrap_text_to_lines(message, MAX_CHARS))
            print ("<"+receivedMessage)
            beep()
        
        keys=getKey(layout)
        if layout == 0:
            layoutName = "a"
        elif layout == 1:
            layoutName = "1"
        elif layout == 2:
            layoutName = "A"
            
        if keys:
            if keys[0] == "alt":
                layout = layout + 1
                ring()
                if layout == 3:
                    layout = 0
                keys[0] = ""
            if keys[0] == "bsp" and cursor == 0:
                text = ""
                return text
            if keys[0] == "bsp":
                if cursor > 0:
                    editText = (editText[0 : cursor - 1]) + (editText[cursor:])
                    cursor = cursor - 1
                while getKey(0):
                    pass
                keys[0] = ""
            if keys[0] == "lt":
                if cursor > 0:
                    cursor = cursor - 1
                keys[0] = ""
            if keys[0] == "rt":
                if cursor < len(editText):
                    cursor = cursor + 1
                keys[0] = ""
            
            if keys[0] == "ent":
                beep()
                text = line
                print (".."+text+" \r",end='')
                return text
            if keys[0] != "":
                if len(editText) < MAX_INPUT_TEXT:
                    editText = (editText[0:cursor]) + keys[0] + (editText[cursor:])
                    cursor = cursor + 1
                    layout = 0
                    while getKey(0):
                        pass
        if len(editText) > 1:
            editMode=">"
        else:
            editMode="#"    
        line = editText  # (editText[0:cursor])+"_"+(editText[cursor:])
        textInput = (editText[0:cursor]) + "_" + (editText[cursor:]) # line[editLine]
        textLen = len(editText)
        maxLine=MAX_CHARS-5
        if textLen > maxLine and cursor > maxLine:
            textInput = (textInput[cursor-maxLine:cursor+1])
        textInput = (textInput[:maxLine+1])
        
        print ((layoutName+editMode)+textInput+" \r", end='')
            
def receiveMessage():
    packet_text = None
    header = [
        0,
        0,
        0,
        0,  # destination
        0,
        0,
        0,
        0,  # sender
        0,
        0,
        0,
        0,  # messageID
        0,
        0,
        0,
        3,
    ]  # Hop limit

    packet = None
    if lora.rx_done():
        packet = lora.receive()
        if len(packet) < 16 :
            print ("short packet")
            return packet_text
        
        header = packet[0:16]
        #print ("To      : %d.%d.%d.%d" % (adrTo3,adrTo2,adrTo1,adrTo0))
        #print ("Received: %d.%d.%d.%d" % (header[0],header[1],header[2],header[3]))
        if header[0] == adrTo3 and header[1] == adrTo2 and header[2] == adrTo1 and header[3] == adrTo0:
            print ("*",end="")
            #return packet_text


        #print("Header:",end="")
        #print(hexlify(header))
        if len(packet) > 16 and packet[16] == 33:  # 33 = sybol !
            #                                        it is delivery confirmation
            #print("Delivery comfirmation")
            #changeMessageStatus(msgID=str(hexlify(packet[8:12]), "utf-8"), old="|S|", new="|D|")
            # do something to mark message is delivered
            packet_text="(ack)"
            return packet_text
        # Decrypt
        cipher = aesio.AES(password, aesio.MODE_CTR, passwordIv)
        inp = bytes(packet[16:])
        outp = bytearray(len(inp))
        cipher.encrypt_into(inp, outp)
        #print("Received encrypted message:")

        try:
            packet_text = str(outp, "utf-8")
        except UnicodeError:
            print("error")  # None
            packet_text = ""
            return packet_text
        #print("Decoded message:")
        #print(packet_text)
        rssi = str(lora.last_rssi)
        snr = str(lora.last_snr)
        destination = hexlify(packet[0:4])
        sender = hexlify(packet[4:8])
        messageID = hexlify(packet[8:12])
        hop = hexlify(packet[12:16])
        timeStamp = str(time.monotonic())
        #print(sender)

        
        try:
            packet_text = str(packet_text, "utf-8")
        except:
            print("Err.")
            print(packet_text)
            return None

        #msrec = str(msrec, 'UTF-8')
        if packet_text != "!":
            sendMessage("!")
        if packet_text == "!":
            packet_text="(ack)"

        ring()
    return packet_text

"""
        # confirmation
        LED.value = True
        # Create response header = swap destination<>sender + same message ID
        header = packet[4:8] + packet[0:4] + packet[8:12] + packet[12:16]
        print("Response header ...")
        print(hexlify(header))
        rfm9x.send(list(bytearray(header + "!")), 0)  # (list(outp), 0)
        print("Confirmation send ...")
        LED.value = False
"""


def sendMessage(text):
    # Header 16 bytes
    header = [
        adrTo3,
        adrTo2,
        adrTo1,
        adrTo0,  # destination
        adrFrom3,
        adrFrom2,
        adrFrom1,
        adrFrom0,  # sender
        msgId3,
        msgId2,
        msgId1,
        msgId0,  # messageID
        0,
        0,
        0,
        3,
    ]  # Hop limit

    # random.randint(min, max)
    outp = bytearray(len(text))
    cipher = aesio.AES(password, aesio.MODE_CTR, passwordIv)
    cipher.encrypt_into(bytes(text, "utf-8"), outp)
    #print("Send header:")
    #print(hexlify(bytearray(header)))
    #print("Encrypted message:")
    #print(hexlify(outp))
    
    #rfm9x.send(list(bytearray(header)) + list(outp), 0)  # (list(outp), 0)
    lora.send(bytearray(header)+bytearray(outp)) #bytes(text,"UTF-8")
    
    #destination = hexlify(bytes(header[0:4]))
    #sender = hexlify(bytes(header[4:8]))
    #messageID = hexlify(bytes(header[8:12]))
    #hop = hexlify(bytes(header[12:16]))
    #timeStamp = str(time.monotonic())  


def showMemory():
    msg = 0
    clearScreen()
    print ( "Message:" + str(len(messages)))

    for s in range(0, 8):           
        if msg < (len(messages)-1):            
            msg = msg + 1
            mem = messages[msg]
            oneItm = mem.split("|")
            direction = ""
            if oneItm[4]== "N":
                direction = "<"
            if oneItm[4]== "S":
                direction = ">" 
            print (direction+oneItm[8])        



def radioInfo():
    #frequency = lora.frequency from CONFIG
    signal_bandwidth =lora.signal_bandwidth
    coding_rate = lora.coding_rate
    spreading_factor = lora.spreading_factor
    preamble_length = lora.preamble_length
    tx_power = lora.tx_power
    print ("Radio info:")
    print ("Frequency:%dMhz Power %ddb" % (frequency, tx_power))
    print ("Country:%s (Preset %s)" % (country, lora_preset))
    print ("CR:%d SF:%d SB:%d" % (coding_rate,spreading_factor,signal_bandwidth))
    print ("Name:(%s)" % (myName))    
    print ("From: %d.%d.%d.%d" % (adrFrom3,adrFrom2,adrFrom1,adrFrom0))
    print ("To: %d.%d.%d.%d" % (adrTo3,adrTo2,adrTo1,adrTo0))
    #pnt20 "12345678901234567890")
    print ("____________________")

# ----------------------FUNCTIONS---------------------------

# with open('x.txt', 'w') as f:
#    f.write("Hello world!\r\n")
#    f.close()



VSYS_voltage = analogio.AnalogIn(board.VOLTAGE_MONITOR)

VBUS_status = digitalio.DigitalInOut(board.VBUS_SENSE)  # defaults to input
VBUS_status.pull = digitalio.Pull.UP  # turn on internal pull-up resistor

SMPSmode = digitalio.DigitalInOut(board.SMPS_MODE)
SMPSmode.direction = digitalio.Direction.OUTPUT
SMPSmode.value = True

# Define pins connected to the chip.
CS = LORA_CS
spi = busio.SPI(LORA_SCK, MOSI=LORA_MOSI, MISO=LORA_MISO)
# Initialze radio
RADIO_FREQ_MHZ = frequency
# Initialze RFM radio
lora = armachat_lora.RFM9x(spi, LORA_CS, RADIO_FREQ_MHZ)
lora.signal_bandwidth=signal_bandwidth
lora.coding_rate=coding_rate
lora.spreading_factor=spreading_factor
lora.preamble_length=preamble_length
lora.tx_power=tx_power
lora.listen()
print ("Armachat System ready ...")
radioInfo()

# Count rising edges only.

while True:


    #keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys1)

    sleepStart_time = time.monotonic()  # fraction seconds uptime
    message = ""
#    while message is None or message == "":
#        sleep_time = time.monotonic() - sleepStart_time
        # if (sleep_time > 10):
        # print ("Sleep in future ...")
        # BACKLIGHT.duty_cycle = 5000
        # time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 3)
        # Deep sleep until the alarm goes off. Then restart the proram.
        # alarm.alarm.light_sleep_until_alarms(time_alarm)

#        keys = keypad.pressed_keys
        # beep()
        # main LOOP
#        message = receiveMessage()
#        if message is not None and not message == "":
#           ring()
#            ring()
#            showMemory()
#        if keys:
            # BACKLIGHT.duty_cycle = 65535
#            break

    text = editor(text="")

    # Most likely there is a max length on the length of text/data
    # that may be sent. Once determined, change code to send chuncks/packets
    if text == "":
        print ("|COMMAND OR MESSAGE|",end="")
        print ("|#  - command      |",end="")
        print ("|>  - message      |",end="")
        print ("|#h - help         |",end="")
        print ("|__________________|",end="")
    if not text == "":
        #pnt20 "12345678901234567890")
        print ("TX>                \r", end='')

        sendMessage(text)
        text = "\n".join(wrap_text_to_lines("--->"+text, MAX_CHARS))
        print (text)

 