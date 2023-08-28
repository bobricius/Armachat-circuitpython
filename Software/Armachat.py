debug = True
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
from adafruit_display_shapes.roundrect import RoundRect
from pwmio import PWMOut
from adafruit_bitmap_font import bitmap_font
from picomputer import *
import digitalio
import random
import armachat_lora

            # ( destination+'|'+sender+'|'+messageID+'|'+hop+'|R|'+rssi+'|'+snr+'|'+
            # timeStamp+'|'+packet_text,'utf-8')

#           |to     | from  |MSGID  |flags  |S|rssi|SNR|timeStamp|text
messages = ["|||||||| Welcome in Armachat: Single leter is implemented as command, longer text is send as message by press [Enter]",
            "0.0.0.0|0.0.0.0|0.0.0.0|0.0.0.0|x|0|0|0| Edit configuration in /lib/config.py do not forget make backup. First command is [H] for HELP"]
addressBook = [
    ['Alpha', '192.168.1.1'],
    ['Beta',  '192.168.1.2'],
    ['Gama',  '192.168.1.3'],
    ['Delta', '192.168.1.4'],
    ['Brota', '255.255.255.255']
]

msgCounter = 0


GUI = True
GUItheme = "white"

########################################################################################
######### MOST IMPORTANT PART - Like main loop, reading keyboard a receiving messages
########################################################################################
def editor(text,helpText,layout):
    cursor = 0
    #layout = 0
    editLine = 0
    editText = text
    editMode = "#"
    layoutName = "a"
    receivedMessage=""
    line = ""
    softKeyIndex=12
    softKey = " .123456789 .abcdefghijklmnopqrstuvwxyz .ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    displayRefresh=True
    sleepStart_time = time.monotonic()  # fraction seconds uptime

    if helpText !="":
        if GUI==True:
            text_window.text=helpText
        else:
            print(helpText)
    while True:
        if time.monotonic() - sleepStart_time > sleepTime:  # every 2 seconds
            display.brightness = sleepBrightness
            if lightSleepEnabled==True:
                goToSleep()
        receivedMessage = None
        radioStatus = ">>"
        if model_lora != "e5":
            if lora.rx_detected():
                radioStatus = "RX"
                displayRefresh=True

            if lora.rx_done():
                debugPrint("RX done")
                receivedMessage = receiveMessage()
                sleepStart_time = time.monotonic()  # fraction seconds uptime
                display.brightness = 1

        if receivedMessage is not None:
            if GUI==True:
                if receivedMessage.count("(OK") == 0:
                    text_window.text="<<"+"\n".join(wrap_text_to_lines(receivedMessage, MAX_CHARS))
                else:
                    text_window.text="<<"+receivedMessage
                setStatusBar()
            else:
                print ("<-"+receivedMessage)
            displayRefresh=True
            beep()

        keys=getKey(layout)

        available = usb_cdc.console.in_waiting
        while available:
            raw = usb_cdc.console.read(available)
            text = raw.decode("utf-8")
            available = usb_cdc.console.in_waiting
            if text.endswith("\n"):
                # strip line end
                text=text.replace("\n", "")
                text=text.replace("\r", "")
                print(bytes(text,'UTF-8'))
                beep()
                return text

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

            if keys == "bsp" and line == "":
                text = "~bsp"
                return text
            if keys == "tab":
                text = "~tab"
                return text
            if keys == "up":
                text = "~up"
                return text            
            if keys == "dn":
                text = "~dn"
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
#             if keys == "up":
#                 cursor = 0
#                 keys = ""
#                 displayRefresh=True
#             if keys == "dn":
#                 cursor = len(editText)
#                 keys = ""
#                 displayRefresh=True

            if keys == "ent":
                beep()
                text = line
                return text
            if keys == "pgdown":
                time.sleep(0.1)
                if softKeyIndex < (len(softKey)-1):
                    softKeyIndex = softKeyIndex + 1
                    
                keys = softKey[softKeyIndex]
                
                editText=editText[:cursor] + keys + editText[cursor+1:]
                displayRefresh=True
                keys = ""            
            if keys == "pgup":
                time.sleep(0.1)
                if softKeyIndex > 0:
                    softKeyIndex = softKeyIndex - 1    
                keys = softKey[softKeyIndex]
                editText=editText[:cursor] + keys + editText[cursor+1:]
                displayRefresh=True
                keys = ""

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
            displayRefresh=False
            if GUI==True:
                cmdMode=len(editText)
                if  cmdMode == 0:
                    editMode="<>"
                elif cmdMode == 1:
                    editMode="#"
                elif cmdMode > 1:
                    editMode=""
                if helpText!="":
                    editMode=""
                text_edit.text=editMode+textInput #layoutName+editMode+
                #text_layout.text=str(textLen)

            else:
                #if display_model== "display280x240" or display_model== "display280x240touch":
                #    layoutName="     "+layoutName  #move text away from rounded corner
                #print ((editMode)+textInput+" \r", end='')
                
                print("\033]0;"+radioStatus+">"+textInput+"\033\\",end="")
def goToSleep():
        display.brightness = 0.001
        time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + timeInLightSleep)
        pin_alarm = alarm.pin.PinAlarm(LORA_INT, value=True, pull=True)
        #print("sleep")
        alarm.light_sleep_until_alarms(time_alarm, pin_alarm)
        #display.brightness = 0.1
        #print("wake")

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

def convertAddress(ip_address):
  # Check if the input string only contains digits and the dot character, and if not, return a default list and False
  if not all(c.isdigit() or c == "." for c in ip_address):
    return [255, 255, 255, 255], False
  # Split the input string by the dot character to get a list of strings
  parts = ip_address.split(".")
  # Check if the input string has exactly 4 parts, and if not, return a default list and False
  if len(parts) != 4:
    return [255, 255, 255, 255], False
  # Create a new list to hold the converted values
  numbers = []
  # Iterate over the list of strings and convert each one to an integer
  for part in parts:
    # Check if the current string is a valid integer between 0 and 255, and if not, return a default list and False
    if not part.isdigit() or int(part) < 0 or int(part) > 255:
      return [255, 255, 255, 255], False
    # Append the converted integer to the list of numbers
    numbers.append(int(part))

  # Return the list of numbers and True
  return numbers, True

def convertMsgID(number):
  # Check if the input number is a valid integer between 0 and 2^32-1, and if not, return a default list
  if not isinstance(number, int) or number < 0 or number > 2**32 - 1:
    return [0, 0, 0, 0]

  # Create a new list to hold the 4 bytes
  bytes = []

  # Iterate over the 4 bytes and append each one to the list of bytes
  for i in range(4):
    # Get the current byte by shifting the input number to the right by 8 * i bits and then taking the lowest 8 bits
    byte = (number >> (8 * i)) & 0xff

    # Append the byte to the list of bytes
    bytes.append(byte)

  # Return the list of bytes
  return bytes

def convertFlags(hops, wantAck):
  # Check that the input number is in the valid range of 0 to 7
  if not (0 <= hops <= 7):
    raise ValueError("Input number must be in the range of 0 to 7")

  # Create a byte array with 3 zeros and the last byte set to the input number
  byte_array = bytearray([0, 0, 0, hops])

  # Set the 4th bit of the last byte to 1 if wantAck is True, or 0 if False
  if wantAck:
    byte_array[3] |= 0b1000
  else:
    byte_array[3] &= 0b0111

  return byte_array

def adjust_name(input_str):
    output_str = input_str[:10]  # truncate the string to the first 10 characters
    num_dashes = 10 - len(output_str)  # calculate the number of dashes to add
    if num_dashes > 0:
        output_str += '-' * num_dashes  # add the necessary number of dashes
    return output_str


### END AICODE
def debugPrint (msg):
    if debug:
        print ("-["+msg+"]")
    if GUI==True:
        text_window.text=msg

def changeMessageStatus(msgID="", old="", new=""):
    global messages
    for i, message in enumerate(messages):
        parts = message.split("|")
        if str(parts[2]) == str(msgID):
            messages[i] = messages[i].replace(old, new)
            debugPrint("Change:"+old+">"+new)


def clearScreen():
    print("\033[2J",end="") #clear screen

def bool2onoff(bvar):
    if bvar == True:
        onoff = "On"
    else:
        onoff = "Off"
    return onoff

def countMessages(msgStat=""):
    if msgStat is None:
        return 0
    allMsg = len(messages)
    c = 0
    for i in range(allMsg):
        if messages[i].count(msgStat) > 0:
            c = c + 1
    return c

def setStatusBar():
    if GUI==True:
        text="SF:"+str(spreading_factor)+" "+country+str(int(frequency))+"Mhz B:"+str(batteryInfo())+"%"+"\n"
        count=countMessages("|R|")
        text=text+"Rx:"+str(count)
        count=countMessages("|S|")
        text=text+" Tx:"+str(count)
        count=countMessages("|D|")
        text=text+" Ack:"+str(count)
        #text_status.text=text


def memoryInfo():
    text="Message memory:\n"
    count=countMessages("|R|")
    text=text+"Received:"+str(count)+"\n"
    count=countMessages("|S|")
    text=text+"Send:"+str(count)+"\n"
    count=countMessages("|D|")
    text=text+"Delivered:"+str(count)
    return text

# def read_serial(serial):
#     available = serial.in_waiting
#     while available:
#         raw = serial.read(available)
#         text = raw.decode("utf-8")
#         available = serial.in_waiting
#     return text

def receiveMessage():

    if model_lora == "e5":
        packet_text = None
        return packet_text

    packet_text = None
    header = [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]

    packet = None
    if lora.rx_done():
        packet = lora.receive()
        if packet is None:
            print("Receiver error")
            return None
        packetSize=len(packet)
        if  packetSize< 16 :
            debugPrint("Short packet <16")
            return packet_text
        debugPrint("Received:"+str(packetSize)+"bytes")
        header = packet[0:16]
        myAdrList, success = convertAddress(myAddress)

        if header[0] == myAdrList[0] and header[1] == myAdrList[1] and header[2] == myAdrList[2] and header[3] == myAdrList[3]:
            debugPrint("My packet")
        else:
            if ignoreDestination==False:
                debugPrint("Not for my")
                return None

        payload = bytes(packet[16:])
        # Decrypt
        if encryption:
            # Decrypt
            cipher = aesio.AES(password, aesio.MODE_CTR, passwordIv)
            outp = bytearray(len(payload))
            cipher.encrypt_into(payload, outp)
            payload=outp
            debugPrint("Decrypted")
        try:
            packet_text = str(payload, "utf-8")
        except UnicodeError:
            print("Unicode Error")  # None
            packet_text = ""
            return packet_text
        #print("Decoded message:")
        #print(packet_text)
        rssi = str(lora.last_rssi)
        snr = str(lora.last_snr)
        destination = str(packet[0])+"."+str(packet[1])+"."+str(packet[2])+"."+str(packet[3])
        sender = str(packet[4])+"."+str(packet[5])+"."+str(packet[6])+"."+str(packet[7])
        msgID =int.from_bytes(packet[8:12], 'big')
        hop = packet[15] & 0b00000111
#         print(sender)
#         print(destination)
#         print(msgID)
#         print(hop)
        try:
            packet_text = str(packet_text, "utf-8")
        except:
            debugPrint("Bad RX data")
            print(packet_text)
            return None

        if packet_text[0] == "!":
            #search in memory if have message with this number with status Send and if yes chage to Delivered
            debugPrint("Ack for:"+str(msgID))
            changeMessageStatus(msgID,"|S|","|D|")
            #update RSSI and SNR
            recResponse = packet_text.split("|")
            ackRSSI=str(recResponse[1])
            ackSNR=str(recResponse[2])
            changeMessageStatus(msgID,"|RSSI|","|"+ackRSSI+"|")
            changeMessageStatus(msgID,"|SNR|","|"+ackSNR+"|")
            packet_text="(OK R:"+ackRSSI+" S:"+ackSNR+")\n      R:"+rssi+" S:"+snr
        elif packet_text[0] == "~":
            debugPrint("Quick MSG")
            packet_text="(OK)\n"+packet_text+"\nR:"+rssi+" S:"+snr
        else:
            debugPrint("Sending ACK")
            ackText="!|"+rssi+"|"+snr
            #swap sender/destination
            sendMessage(sender,destination,msgID,maxHops,False,ackText)
            debugPrint("RX saved")
            timeStamp=int(time.monotonic())
            receivedMsg =str(destination+"|"+sender+"|"+str(msgID)+"|"+str(hop)+"|R|"+rssi+"|"+snr+"|"+str(timeStamp)+"|"+packet_text)
            #debugPrint(receivedMsg)
            messages.append(receivedMsg)
            ring()
    return packet_text

def sendMessage(destination="",sender="",msgID=0,hops=0,wantAck=True,text=""):

    adrDestination, success = convertAddress(destination)
#     if success:
#         print(numbers) # [192, 168, 0, 1]
#     else:
#         print("Bad Destination address")
    adrSender, success = convertAddress(sender)
#     if success:
#         print(numbers) # [192, 168, 0, 1]
#     else:
#         print("Bad Destination address")
    # random.randint(min, max)
    adrDestination=bytearray(adrDestination)
    adrSender=bytearray(adrSender)
    msgIDlist=bytearray(convertMsgID(msgID))
    flagsList=bytearray(convertFlags(hops, wantAck))
    payload = bytearray(text)
    if encryption:
        cipher = aesio.AES(password, aesio.MODE_CTR, passwordIv)
        cipher.encrypt_into(bytes(text, "utf-8"), payload)
        debugPrint("Encrypted")

    header=bytearray(adrDestination+adrSender+msgIDlist+flagsList)
    debugPrint("TX "+str(16+len(payload))+"b")
    while lora.rx_detected():
        debugPrint("Channel busy")
        if lora.rx_done():
            debugPrint("RX inside TX")
            receivedMessage = receiveMessage()
            if receivedMessage is not None:
                print ("<-"+receivedMessage)
                beep()
#         rndWait=random.random()
#         debugPrint("TX random wait "+str(rndWait)+"s")
#         time.sleep(rndWait)
    start_time = time.monotonic()
    if model_lora != "e5":
        lora.send(bytearray(header)+bytearray(payload)) #bytes(text,"UTF-8")
    stop_time = time.monotonic()
    debugPrint("TX done "+str(stop_time - start_time)+"sec.")
    if text[0] == "!":
        debugPrint("Received ACK")
    elif text[0] == "~":
        debugPrint("Send QUICK MSG")
    else:
        debugPrint("TX saved")
        timeStamp=int(time.monotonic())
        storedMsg =str(destination+"|"+sender+"|"+str(msgID)+"|"+str(hops)+"|S|RSSI|SNR|"+str(timeStamp)+"|"+text)
        #debugPrint(storedMsg)
        messages.append(storedMsg)

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

def displayMessage(index=0, details=True):
        values = messages[index].split("|")
        msgStatus=values[4]
        if msgStatus=="R":
          msgStatus="<-"
        elif msgStatus=="S":
          msgStatus="? "
        elif msgStatus=="D":
          msgStatus="->"
        msgText=values[-1]
        addFromTo = ">".join(values[0:2])
        if GUI==True:
            textW = str(index)+"#"+msgStatus+msgText
            textW = "\n".join(wrap_text_to_lines(textW, MAX_CHARS))
            text_window.text=textW
        else:
            if details==True:
                print(str(index)+"# "+addFromTo)
                print(msgStatus+values[-1]) #text
                print("RSSI:"+values[5]+" SNR:"+values[6] )
            else:
                print(str(index)+"#"+msgStatus+msgText) #text
        return msgText


def radioInfo():
    #frequency = lora.frequency from CONFIG
    text=""
    if model_lora != "e5":
        signal_bandwidth =lora.signal_bandwidth
        coding_rate = lora.coding_rate
        spreading_factor = lora.spreading_factor
        preamble_length = lora.preamble_length
        tx_power = lora.tx_power

        text = text+ ("Freq:%dMhz Power:%ddb" % (frequency, tx_power)+ "\n")
        #print ("Country:%s (Preset %s)" % (country, lora_preset))
        text = text+ ("CR:%d SF:%d SB:%d" % (coding_rate,spreading_factor,signal_bandwidth)+ "\n")
        text = text+ ("Name:(%s)" % (myName)+ "\n")
        text = text+ ("From:"+myAddress + "\n")
        text = text+ ("To:"+destination + "\n")
        return text
def pingBeacon():
    counter=0
    ring()
    if GUI==True:
        text_edit.text="[Q] to exit"
    else:
        print("\033]0;    [Q] to exit Beacon \033\\")
    while getKey(0)!= "q":
        msgID=random.randint(0, 2147483647)
        text="~"+str(counter)
        counter = counter+1
        sendMessage(myAddress,destination,msgID,maxHops,True,text)
        if GUI==True:
            text_window.text=text
        else:
            print(text)
    ring()
    return

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
def saveConfig():
    configKey=34 #
    cfgDestination, success = convertAddress(destination)
    NVMdata =bytearray([configKey,spreading_factor,tx_power,country_code]+cfgDestination)
    print(NVMdata)
    microcontroller.nvm[0:len(NVMdata)] = NVMdata
    debugPrint("Save config to NVM")
# ----------------------FUNCTIONS---------------------------


############################################################################
######### SETUP - Program start
############################################################################
print("\033]0;   Loading ....\033\\")
#check if is correct configuration KEY
if microcontroller.nvm[0]==34:
    #configuration load from NVM
    print ("Loading NVM config")
    spreading_factor=microcontroller.nvm[1]
    tx_power=microcontroller.nvm[2]
    destination=str(microcontroller.nvm[4])+"."+str(microcontroller.nvm[5])+"."+str(microcontroller.nvm[6])+"."+str(microcontroller.nvm[7])
    country_code==microcontroller.nvm[3]
    if country_code==1:
        country="EU"
    else:
        country="US"

board_type = os.uname().machine
print (board_type)
if 'rp2040' in board_type:
    VSYS_voltage = analogio.AnalogIn(board.VOLTAGE_MONITOR)
    VBUS_status = digitalio.DigitalInOut(board.VBUS_SENSE)  # defaults to input
    VBUS_status.pull = digitalio.Pull.UP  # turn on internal pull-up resistor
    SMPSmode = digitalio.DigitalInOut(board.SMPS_MODE)
    SMPSmode.direction = digitalio.Direction.OUTPUT
    SMPSmode.value = True
    #LED = digitalio.DigitalInOut(board.GP25)
    #LED.direction = digitalio.Direction.OUTPUT

############################################################################
######### Resize terminal
############################################################################
if GUI==True:
    # Create a Group
    mygroup = displayio.Group()
    print("Starting GUI...")
#     display.show(None)
#     splash = display.root_group # this gets the current root_group, the REPL
    display.show(mygroup)
#     supervisor.reset_terminal(display.width, 60+24) #+12
#     splash.y=180-12 # -12
#     print("Resize and move terminal ....")
#     mygroup.append(splash)

    font_file = "fonts/neep-24.pcf" 
    #font_file = "fonts/gomme-20.pcf"
    #font_file = "fonts/pavlova-16.pcf"
    font = bitmap_font.load_font(font_file)
    terminal_font = terminalio.FONT
    
    if GUItheme=="white":
        WindowColor=0xFFFFFF
        TextColor=0x000000
    else:
        WindowColor=0x000000
        TextColor=0xFFFFFF
        
    #status_roundrect = RoundRect(40, 0, 158, 22, 4, fill=0x101010, outline=0x00FF00, stroke=1)
    window_roundrect = RoundRect(0, 32, display.width, 208, 4, fill=WindowColor, outline=0xFF0FFF, stroke=1)
    edit_roundrect = RoundRect(0, 0, display.width, 30, 4, fill=WindowColor, outline=0x0F00FF, stroke=1)
    #layout_roundrect = RoundRect(200, 0, 50, 22, 4, fill=0xA0A0A0, outline=0xFF0000, stroke=1)

    text_window = bitmap_label.Label(font, line_spacing=1, text="#  command\n#h HELP\n _ lowercase\n | symbol\n - uppercase\nESC - GUI/Terminal", color=TextColor, x=1, y=44)
    text_edit = bitmap_label.Label(font, line_spacing=1, text="TEXT", color=TextColor, x=2, y=14)
    #text_status = bitmap_label.Label(terminal_font, line_spacing=1, text="Armachat\nMESSENGER", color=0xFFFFFF, x=48, y=5)
    #text_layout = bitmap_label.Label(font, line_spacing=1, text="ABC", color=TextColor, x=205, y=9)


    mygroup.append(window_roundrect)
    #mygroup.append(status_roundrect)
    mygroup.append(edit_roundrect)
    #mygroup.append(layout_roundrect)
    mygroup.append(text_window)
    mygroup.append(text_edit)
    #mygroup.append(text_status)
    #mygroup.append(text_layout)
############################################################################
######### Start loop
############################################################################

#supervisor.set_next_code_file("ArmachatGUI.py")

# Define pins connected to the chip.
if model_lora != "e5":
    spi = busio.SPI(LORA_SCK, MOSI=LORA_MOSI, MISO=LORA_MISO)
    RADIO_FREQ_MHZ = frequency
    print("LoRa init...")
    try:
        lora = armachat_lora.RFM9x(spi, LORA_CS, RADIO_FREQ_MHZ)
    except:
        print(">Error")
        #searching alternative module position
        #if you use SD card
        try:
            print("LoRa alternative...")
            lora = armachat_lora.RFM9x(spi, RXD, RADIO_FREQ_MHZ)
        except:
            print(">No LoRa")
            model_lora="e5"

if model_lora != "e5":
    print("-LoRa ready")
    lora.signal_bandwidth=signal_bandwidth
    lora.coding_rate=coding_rate
    lora.spreading_factor=spreading_factor
    lora.preamble_length=preamble_length
    lora.tx_power=tx_power
    lora.low_datarate_optimize=1
    lora.listen()
    print (radioInfo())

print ("Armachat ready ...")
print (" #   - command")
print (" >   - message")
print (" #h  - help")
print (" ESC - GUI/Terminal")

############################################################################
######### MAIN LOOP
############################################################################
lastMessage =0
message = ""
messageDetails=True

#     def idle(self) -> None:
#         """Enter idle standby mode."""
#         self.operation_mode = STANDBY_MODE
#
#     def sleep(self) -> None:
#         """Enter sleep mode."""
#         self.operation_mode = SLEEP_MODE
#
#     def listen(self) -> None:
#         """Listen"""

while True:
    ### most important part, editor checking keyboard and receiving messages
    text = editor(text=message, helpText="", layout=0)
    setStatusBar()
    #clearScreen()
    if text=="~up":
        clearScreen()
        lastMessage = max(0, lastMessage - 1)
        displayMessage(lastMessage,messageDetails)
        continue
    if text=="~dn":
        clearScreen()
        lastMessage = min(len(messages) - 1, lastMessage + 1)
        displayMessage(lastMessage,messageDetails)
        continue
    if text == "~tab" or text=="~bsp":
        GUI = not GUI
        if GUI==True:
            display.show(mygroup)
        else:
            display.show(None)
        ring()
        continue

    if len(text) == 1:
        #clearScreen()
        if text == "h":
            clearScreen()
            #[G]ping [P]Profile [F]Frequency
            cmdInfo = "[E]edit [M]Memory [L]List [R]Radio\n[C]Crypto [D]Debug [G]Ping [V]Receive all [S]SF [P]Power [B] Battery [I]Storage [A]Address to"
            cmdInfo = "\n".join(wrap_text_to_lines(cmdInfo, MAX_CHARS))
        elif text == "c":
            encryption = not encryption
            cmdInfo = "Enctryption:"+bool2onoff(encryption)
        elif text == "e":
            cmdInfo = "Editing message:"+str(lastMessage)
            message = displayMessage(lastMessage,False)
        elif text == "d":
            debug = not debug
            cmdInfo = "Debug messages:"+bool2onoff(debug)
        elif text == "v":
            ignoreDestination = not ignoreDestination
            cmdInfo = "Receive all:"+bool2onoff(ignoreDestination)
        elif text == "s":
            ring()
            text = editor(text=str(spreading_factor),helpText="Spread factor:", layout=0)
            if not text.isdigit() or int(text) < 6 or int(text) > 12:
                cmdInfo = "Error: 6-12"
            else:
                cmdInfo = "SF changed:\n"+text
                spreading_factor=int(text)
                saveConfig()
                lora.spreading_factor=spreading_factor
        elif text == "p":
            ring()
            text = editor(text=str(tx_power),helpText="TX power:", layout=0)
            if not text.isdigit() or int(text) < 5 or int(text) > 23:
                cmdInfo = "Error: 5-23"
            else:
                cmdInfo = "Power changed:\n"+text
                tx_power=int(text)
                saveConfig()
                lora.tx_power=tx_power

        elif text == "m":
            cmdInfo = memoryInfo()
        elif text == "l":
            messageDetails = not messageDetails
            cmdInfo = "Message Details:"+bool2onoff(messageDetails)
        elif text == "r":
            cmdInfo = radioInfo()
        elif text == "i":
            cmdInfo = filesystemInfo()
        elif text == "w":
            cmdInfo = "nothing"
        elif text == "b":
            cmdInfo = powerInfo()
            cmdInfo = cmdInfo+"Capacity:"+str(batteryInfo())+"%"
        elif text == "g":
            pingBeacon()
            cmdInfo = "Beacon finished"
        elif text == "n":
            text = editor(text=myName,helpText="Enter your IDname:", layout=0)
            myName=adjust_name(text)
            cmdInfo = "You are now:\n"+myName
        elif text == "a": #addresbook experiment
            abook = ""
            for i, row in enumerate(addressBook):
                abook = abook+ (str(i)+"."+addressBook[i][0]+"-"+addressBook[i][1]+"\n")
            text = editor(text="",helpText=abook, layout=1)
            if not text.isdigit() or int(text) < 0 or int(text) > 4:
                cmdInfo = "Error: 0-4"
            else:
                destAdr=int(text)
                destination=addressBook[destAdr][1]
                cmdInfo = "Selected:\n"+addressBook[destAdr][0]+"\n"+destination+"\n"
                saveConfig()

        elif text == "t": #destination
            text = editor(text=destination,helpText="Enter address:", layout=0)
            adrDestination, success = convertAddress(text)
            if success:
                cmdInfo = "Destination changed:\n"+text
                destination=text
                saveConfig()
            else:
                cmdInfo = "Bad Destination address"

        else:
            cmdInfo = "Try for [H] help"

        if GUI==True:
            text_window.text=cmdInfo
        else:
            print(cmdInfo)
        setStatusBar()
        ring()
        ring()
    else:
        msgID=random.randint(0, 2147483647)
        sendMessage(destination,myAddress,msgID,maxHops,True,text)
        text = "\n".join(wrap_text_to_lines("->"+text, MAX_CHARS))

        if GUI==True:
            text_window.text=text
        else:
            print (text)

        message = ""
        lastMessage=len(messages)-1

