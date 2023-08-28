import time
import board
import busio
import terminalio
import displayio
import os
import gc
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
    print("MENU:")
    for i in range(0, max_length, 1):
        print("     "+menu_options[i].rsplit('.', 1)[0])   #[0:10]
    print("[ Select app ]")
    updateStatus(SCALE)
    return max_length

menu_options = file_filter(os.listdir())
max_length = len(menu_options)

supervisor.runtime.autoreload = False
print("\033[2J",end="") #clear screen
printMenu(menu_options)

#print("\033[5;15H",end="")
#ESC [ nnnn ; mmmm H
#print("[Select by 0-9]")
menu=0
#supervisor.status_bar.display = False
while True:
    keys=getKey(0) #keyboard layout 1 = symbols and numbers
    if keys:
        if keys == "up":
            if menu > 0:
                menu = menu - 1
        if keys == "dn":
            if menu < max_length-1:
                menu = menu + 1
        while getKey(0):
            pass
            #beep()
    print("\033["+str(menu+2)+";0H",end="")
    print("--> [",end="")
    print("\033["+str(menu+2)+";20H",end="")
    print("]",end="")
    time.sleep(0.05)
    print("\033["+str(menu+2)+";0H",end="")
    print("     ",end="")
    print("\033["+str(menu+2)+";20H",end="")
    print(" ",end="") 
    if keys=="g":
        GUI = not GUI
        updateStatus(SCALE)
        ring()
        continue
    if keys=="s":
            display.root_group.scale = 2
            supervisor.reset_terminal(display.width,120)
            SCALE=2
            updateStatus(SCALE)
            printMenu(menu_options)
            ring()
            continue
    if keys=="ent":
        startApp=(menu_options[menu])
        supervisor.set_next_code_file(startApp)
        print("\033[2J",end="") #clear screen
        print("Free memory:"+str(gc.mem_free()))
        print("Next boot set to:")
        print(startApp)
        try:
            gc.collect()
            exec(open(startApp).read())
        except Exception as err:
            print(err)
        print("Program finished ...")
        print("\033[2J",end="") #clear screen
        printMenu(menu_options)

