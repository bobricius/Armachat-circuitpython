# Armachat-circuitpython
New Armachat based on Raspberry Pi PICO an Circuitpython code

**Software working features:**

- send message with header and store to memory
- receive message and parse header, store to memory
- display message memory with message details like SNR and RSSI
- count messages in memory by type
- display some hardware details like free memory and power supply voltage, it is good for future battery operation
- Terminal display with messages from background systems
- AES256 encryption
- message confirmation and status change in memory
- boot safe mode


**TODO:**

- Need much better LoRa library with, CAD, status detection, and INTERRUPT !!!
- contact list
- setup and save configuration
- save memory to flash



##Fixes in this repository

- Much more stable
- Formatting changes in all three files. I'm using the Mu editor, <a href="https://codewith.mu/">https://codewith.mu/</a>, that has Check and Tidy functions to help standardize formatting. The formatting changes are from using those functions in the Mu editor.

**boot.py**

- Pull model information from config.py to obtain the model and keyboard setup information.
- Used the adafruit_matrixkeypad to scan the keyboard.
- Display prompts based on the Armachat model
- Added a progress bar to show remaining time to make a selection for safe and write modes.

**code.py**

- Added a function named screenSafeText, which removed characters from a string that is a non-printable character. There were some random errors due to received messages having non-printable characters. When the messages were displayed, there would be no font in the font file for them, which would cause the code to crash.
- Added a 0.1 second delay when checking for a key press. I was experiencing skipping screens as the left or right button (bsp, ent) was read twice or more on one key press. This is not a perfect solution but the results in a better user experience.
- Added try/catch blocks around attempts to read or write files. I would have rather used file exists for reads but it appears that CircuitPython's file library does not have an exists function. The use of try/catch blocks appears to be the preferred method to check for a file's existence.
- Created the function radioInit to allow changing of the LoRa radio on the fly.
- Added the CPU Temperature from Kayto's code
- Added the Ping function from Kayto's code
- Allow changing the frequency on the fly
- Allow changing the power on the fly
- Matched LoRa profiles to Meshtastic's profiles

**config.py**

- No changes other than format

BTW: Save memory to flash does work if you change the file system to write mode by pressing the ALT key when booting and pressing the S key when viewing messages.