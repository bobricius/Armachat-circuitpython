import board
import time
from pwmio import PWMOut

def beep():
        audioPin = PWMOut(board.GP0, duty_cycle=0, frequency=440, variable_frequency=True)
        audioPin.frequency = 5000
        audioPin.duty_cycle = 60000
        time.sleep(0.002)
        audioPin.duty_cycle = 0
        audioPin.deinit()


def ring():
        audioPin = PWMOut(board.GP0, duty_cycle=0, frequency=440, variable_frequency=True)
        audioPin.frequency = 2000
        audioPin.duty_cycle = 60000
        time.sleep(0.1)
        audioPin.frequency = 3000
        audioPin.duty_cycle = 60000
        time.sleep(0.1)
        audioPin.frequency = 6000
        audioPin.duty_cycle = 60000
        time.sleep(0.1)
        audioPin.duty_cycle = 0
        audioPin.deinit()
