import time
import board
import busio
import terminalio
import displayio
import os
import microcontroller
import digitalio
import supervisor

GUI=True
SCALE=1

from picomputer import *

hidden_ID = ['.', '_', 'TRASH', 'boot_out.txt', 'main.py', 'code.py', 'menu.py', 'main.txt', 'code.txt', 'boot.py']         # List of file name elements and names we do not want to see
#pnt20"")
#print("\033]0;   DOS - Doomsday Operating System\033\\")

def updateStatus(fontSize):
    if GUI == True:
        onoff = "GUI=On"
    else:
        onoff = "GUI=Off"
    if SCALE==1:
        print("\033]0;   DOS - Doomsday Operating System "+onoff+" Font:"+str(fontSize)+"\033\\",end="")
    else:
        print("\033]0;DoomsdayOperatingSystem\033\\",end="")
    return

def file_filter(data):
    for y in hidden_ID:
        filtered_data = [x for x in data if not x.startswith(y)]
        data = filtered_data
    filtered_data = [x for x in data if x[-3:] == '.py' or x[-4:] == '.txt' ]
    return sorted(filtered_data)

def printMenu(menu_options):
    max_length = len(menu_options)

    for i in range(0, max_length, 1):
            print( "[{}] {}".format(i, menu_options[i]))
    if SCALE==1:
        print("[Select by 0-9][G-GUI][F-Font]")
    else:
        print("[Select by 0-9]")
    updateStatus(SCALE)
    return max_length

menu_options = file_filter(os.listdir())
max_length = len(menu_options)

printMenu(menu_options)

while True:

    keys=getKey(1) #keyboard layout 1 = symbols and numbers
    if keys=="%":
        GUI = not GUI
        updateStatus(SCALE)
        ring()
        continue
    if keys=="$":
            display.root_group.scale = 2
            supervisor.reset_terminal(display.width,120)
            SCALE=2
            updateStatus(SCALE)
            printMenu(menu_options)
            ring()
            continue
    if keys:
        try:
            selected =int(keys)
            beep()
        except Exception:
            selected = 0
    
        if selected<max_length:
            supervisor.set_next_code_file(menu_options[selected])
            print("Next boot set ...")
            # and then if you want to run it now, trigger a reload
            #supervisor.reload() 
            #text="a=1\nb=3\nprint(a+b)"
            try:
                exec(open(menu_options[selected]).read())
                #print(text)
                #exec(text)
            except Exception as err:
                print(err)
            print("Program finished ...")
            while True:
                pass


            
            