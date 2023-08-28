"""
CircuitPython single MP3 playback example for Raspberry Pi Pico.
Plays a single MP3 once.
"""
import board
import audiomp3
import audiopwmio
from picomputer import *

audio = audiopwmio.PWMAudioOut(AUDIO_GPIO)

print("Done playing!")
decoder = audiomp3.MP3Decoder(open("/mp3/new.mp3", "rb"))

audio.play(decoder)
while audio.playing:
    pass