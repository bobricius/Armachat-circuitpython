import board
import digitalio
import os

unitName = "ARMACHAT"
freq = 915.0
power = 23

# Matches Mestastic values in table at
# https://meshtastic.org/docs/settings/channel
# 1 => Bw500Cr45Sf128       Short/Fast
# 2 => Bw125Cr45Sf128       Short/Slow
# 3 => Bw250Cr47Sf1024      Medium/Fast
# 4 => Bw250Cr46Sf2048      Medium/Slow
# 5 => Bw31_25Cr48Sf512     Long/Fast
# 6 => Bw125Cr48Sf4096      Long/Slow

loraProfile = 1

myName = "DemoUser"

myGroup3 = 0x03
myGroup2 = 0x02
myGroup1 = 0x01
myID = 1

dest3 = 0x13
dest2 = 0x12
dest1 = 0x11
dest0 = 0

msgId3 = 0x13
msgId2 = 0x12
msgId1 = 0x11
msgId0 = 0

password = "Sixteen byte key"
passwordIv = "Sixteen byte key"
bright = 1
sleep = 0
font = 2
theme = 1

volume = 6

maxLines = 6
maxChars = 26

model = "compact"
# model = "max"

if model == "compact":
    cols = [
        digitalio.DigitalInOut(x)
        for x in (board.GP1, board.GP2, board.GP3, board.GP4, board.GP5)
    ]
    rows = [
        digitalio.DigitalInOut(x)
        for x in (board.GP6, board.GP9, board.GP15, board.GP8, board.GP7, board.GP22)
    ]
    keys1 = (
        ("ent", " ", "m", "n", "b"),
        ("bsp", "l", "k", "j", "h"),
        ("p", "o", "i", "u", "y"),
        ("alt", "z", "x", "c", "v"),
        ("a", "s", "d", "f", "g"),
        ("q", "w", "e", "r", "t"),
    )

    keys2 = (
        ("rt", ",", ">", "<", '""'),
        ("lt", "-", "*", "&", "+"),
        ("0", "9", "8", "7", "6"),
        ("alt", "(", ")", "?", "/"),
        ("!", "@", "#", "$", "%"),
        ("1", "2", "3", "4", "5"),
    )

    keys3 = (
        ("dn", ";", "M", "N", "B"),
        ("up", "L", "K", "J", "H"),
        ("P", "O", "I", "U", "Y"),
        ("alt", "Z", "X", "C", "V"),
        ("A", "S", "D", "F", "G"),
        ("Q", "W", "E", "R", "T"),
    )

else:
    cols = [
        digitalio.DigitalInOut(x)
        for x in (board.GP1, board.GP2, board.GP3, board.GP4, board.GP5, board.GP14)
    ]
    rows = [
        digitalio.DigitalInOut(x)
        for x in (board.GP6, board.GP9, board.GP15, board.GP8, board.GP7, board.GP22)
    ]
    keys1 = (
        (" ", ".", "m", "n", "b", "dn"),
        ("ent", "l", "k", "j", "h", "lt"),
        ("p", "o", "i", "u", "y", "up"),
        ("bsp", "z", "x", "c", "v", "rt"),
        ("a", "s", "d", "f", "g", "tab"),
        ("q", "w", "e", "r", "t", "alt"),
    )

    keys2 = (
        ("_", ",", ">", "<", '""', "{"),
        ("~", "-", "*", "&", "+", "["),
        ("0", "9", "8", "7", "6", "}"),
        ("=", "(", ")", "?", "/", "]"),
        ("!", "@", "#", "$", "%", "\\"),
        ("1", "2", "3", "4", "5", "alt"),
    )

    keys3 = (
        (":", ";", "M", "N", "B", "dn"),
        ("ent", "L", "K", "J", "H", "lt"),
        ("P", "O", "I", "U", "Y", "up"),
        ("bsp", "Z", "X", "C", "V", "rt"),
        ("A", "S", "D", "F", "G", "tab"),
        ("Q", "W", "E", "R", "T", "alt"),
    )

# ----------         End of Settings          ----------
# ---------- Start read/write config.txt file ----------

# File Open Modes
# r -> read
# rb -> read binary
# w -> write
# wb -> write binary
# a -> append
# ab -> append binary

CONFIG_FILENAME = "config.txt"

config_settings = set()
config_excludeNames = {
    "CONFIG_FILENAME",
    "__file__",
    "__name__",
    "maxChars",
    "maxLines",
    "model"
}
config_includeTypes = {
    float,
    int,
    str
}


def fileExists(fileName):
    retVal = False

    try:
        with open(fileName, "r") as f:
            f.readlines()
            retVal = True
    except OSError:
        print(fileName + " does not exist")

    return retVal


def fileSystemWriteMode():
    retVal = False
    testFileName = "delete.txt"

    try:
        with open(testFileName, "w") as f:
            f.write("test\n")
            retVal = True

        os.remove(testFileName)
    except OSError:
        print("Read Only File System")

    return retVal


def getConfigProperties():
    my_globals = globals()
    for g in my_globals:
        if g not in config_excludeNames:
            if type(globals()[g]) in config_includeTypes:
                config_settings.add(g)


# printConfigProperties is useful for debugging and may be removed
def printConfigProperties():
    i = 1
    for c in config_settings:
        # print(str(i) + chr(9) + c + chr(9) + str(globals()[c]))

        if str(type(globals()[c])) == "<class 'str'>":
            print(c + " = \"" + str(globals()[c]) + "\"")
        else:
            print(c + " = " + str(globals()[c]))
        i = i + 1


def readConfig(createIfNotExists=False):
    if len(config_settings) == 0:
        getConfigProperties()

    if not fileExists(CONFIG_FILENAME):
        if createIfNotExists:
            writeConfig()
        return False

    with open(CONFIG_FILENAME, "r") as f:
        conf = f.readlines()
        print("Reading config:")
        for line in conf:
            if line.strip().startswith("#"):  # Ignore comment
                continue

            keyvalPair = line.split("=")

            if(len(keyvalPair) != 2):  # Ignore not key value pair
                continue

            key = keyvalPair[0].strip()
            value = keyvalPair[1].strip()

            if key not in config_settings:  # Ignore key is not a setting
                continue

            if isinstance(globals()[key], str):
                if value.startswith("\"") and value.endswith("\""):
                    value = value[1:-1]
                globals()[key] = value
            elif isinstance(globals()[key], int):
                globals()[key] = int(value)
            elif isinstance(globals()[key], float):
                globals()[key] = float(value)

    return True


def writeConfig():
    if len(config_settings) == 0:
        getConfigProperties()

    if not fileSystemWriteMode():
        print("Cannot write config file.")
        print("Enable Write mode on device boot.")
        return False

    # Recover from previous failure #
    # If the old config file exists, assume a failure last time.
    # Copy the old config file back and try again.
    # This will cause an issue if the original configuration file
    # was the source of the issue and the code has not changed to
    # address the issue.
    if fileExists(CONFIG_FILENAME + ".old"):
        if fileExists(CONFIG_FILENAME):
            os.remove(CONFIG_FILENAME)
        os.rename(CONFIG_FILENAME + ".old", CONFIG_FILENAME)

    # if the config file exists, rename it then delete it
    if fileExists(CONFIG_FILENAME):
        os.rename(CONFIG_FILENAME, CONFIG_FILENAME + ".old")

    # Create dict to track if items have been saved
    configTrackDict = {}
    for k in config_settings:
        configTrackDict[k] = False

    with open(CONFIG_FILENAME + ".old", "r") as f_old:
        with open(CONFIG_FILENAME, "w") as f_new:
            conf_old = f_old.readlines()
            for line in conf_old:
                if line.strip().startswith("#"):  # Comment
                    if line.endswith("\n"):
                        f_new.write(line)
                    else:
                        f_new.write(line + "\n")
                    continue

                keyvalPair = line.split("=")
                if(len(keyvalPair) != 2):  # Not key value pair
                    if line.endswith("\n"):
                        f_new.write(line)
                    else:
                        f_new.write(line + "\n")
                    continue

                key = keyvalPair[0].strip()

                if key not in config_settings:  # Ignore key is not a setting
                    if line.endswith("\n"):
                        f_new.write(line)
                    else:
                        f_new.write(line + "\n")
                    continue

                if isinstance(globals()[key], str):
                    f_new.write(key + " = \"" + globals()[key] + "\"\n")
                    configTrackDict[key] = True
                else:
                    f_new.write(key + " = " + str(globals()[key]) + "\n")
                    configTrackDict[key] = True

            for dkey, dval in configTrackDict.items():
                if not dval:
                    if isinstance(globals()[dkey], str):
                        f_new.write(dkey + " = \"" + globals()[dkey] + "\"\n")
                    else:
                        f_new.write(dkey + " = " + str(globals()[dkey]) + "\n")

    if fileExists(CONFIG_FILENAME + ".old"):
        os.remove(CONFIG_FILENAME + ".old")

    return True


# print("--- Default Settings ---")
# printConfigProperties()
readConfig()
# print("--- Configuration File Settings ---")
# printConfigProperties()

# writeConfig()
