import board
import digitalio
    #Bw125Cr45Sf128 = (0x72, 0x74, 0x04) #< Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on. Default medium range
    #Bw500Cr45Sf128 = (0x92, 0x74, 0x04) #< Bw = 500 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on. Fast+short range
    #Bw31_25Cr48Sf512 = (0x48, 0x94, 0x04) #< Bw = 31.25 kHz, Cr = 4/8, Sf = 512chips/symbol, CRC on. Slow+long range
    #Bw125Cr48Sf4096 = (0x78, 0xc4, 0x0c) #/< Bw = 125 kHz, Cr = 4/8, Sf = 4096chips/symbol, low data rate, CRC on. Slow+long range
    #Bw125Cr45Sf2048 = (0x72, 0xb4, 0x04) #< Bw = 125 kHz, Cr = 4/5, Sf = 2048chips/symbol, CRC on. Slow+long range
    #Bw31Cr48Sf4096 = (0x48, 0xc4, 0x04) #< Bw = 125 kHz, Cr = 4/5, Sf = 2048chips/symbol, CRC on. Slow+Extra long range


unitName ="ARMACHAT"
freq = 868.0
spread = 10
power = 23
bandwidth = 41700
codingRate = 8


myName ="DemoUser"

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

password = b'Sixteen byte key'
passwordIv = b'Sixteen byte key'
bright = 1
sleep = 0
font = 2
theme = 1

volume = 6

maxLines = 6
maxChars = 26

model = "compact"
#model = "max"

if model=="compact":
	cols = [digitalio.DigitalInOut(x) for x in (board.GP1, board.GP2, board.GP3, board.GP4, board.GP5)]
	rows = [digitalio.DigitalInOut(x) for x in (board.GP6, board.GP9, board.GP15, board.GP8, board.GP7, board.GP22)]
	keys1 =  (('ent', ' ', 'm', 'n', 'b'),
			 ("bsp", 'l', 'k', 'j', 'h'),
			 ('p', 'o', 'i', 'u', 'y'),
			 ("alt", 'z', 'x', 'c', 'v'),
			 ('a', 's', 'd', 'f', 'g'),
			 ('q', 'w', 'e', 'r', 't'))  

	keys2 =  (('rt', ',', '>', '<','""'),
			 ('lt', '-', '*', '&', '+'),
			 ('0', '9', '8', '7', '6'),
			 ('alt', '(', ')', '?', '/'),
			 ('!', '@', '#', '$', '%'),
			 ('1', '2', '3', '4', '5'))

	keys3 =  (('dn', ';', 'M', 'N', 'B'),
			 ("up", 'L', 'K', 'J', 'H'),
			 ('P', 'O', 'I', 'U', 'Y'),
			 ("alt", 'Z', 'X', 'C', 'V'),
			 ('A', 'S', 'D', 'F', 'G'),
			 ('Q', 'W', 'E', 'R', 'T')) 

else:
	cols = [digitalio.DigitalInOut(x) for x in (board.GP1, board.GP2, board.GP3, board.GP4, board.GP5, board.GP14)]
	rows = [digitalio.DigitalInOut(x) for x in (board.GP6, board.GP9, board.GP15, board.GP8, board.GP7, board.GP22)]
	keys1 =  ((' ', '.', 'm', 'n', 'b',"dn"),
			 ("ent", 'l', 'k', 'j', 'h',"lt"),
			 ('p', 'o', 'i', 'u', 'y',"up"),
			 ("bsp", 'z', 'x', 'c', 'v',"rt"),
			 ('a', 's', 'd', 'f', 'g',"tab"),
			 ('q', 'w', 'e', 'r', 't',"alt"))  

	keys2 =  (('_', ',', '>', '<','""','{'),
			 ('~', '-', '*', '&', '+','['),
			 ('0', '9', '8', '7', '6','}'),
			 ('=', '(', ')', '?', '/',']'),
			 ('!', '@', '#', '$', '%','\\'),
			 ('1', '2', '3', '4', '5',"alt"))

	keys3 =  ((':', ';', 'M', 'N', 'B',"dn"),
			 ("ent", 'L', 'K', 'J', 'H',"lt"),
			 ('P', 'O', 'I', 'U', 'Y',"up"),
			 ("bsp", 'Z', 'X', 'C', 'V',"rt"),
			 ('A', 'S', 'D', 'F', 'G',"tab"),
			 ('Q', 'W', 'E', 'R', 'T',"alt")) 
