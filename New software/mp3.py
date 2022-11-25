"""
CircuitPython single MP3 playback example for Raspberry Pi Pico.
Plays a single MP3 once.
"""
import board
import audiomp3
import audiopwmio

audio = audiopwmio.PWMAudioOut(board.GP0)

decoder = audiomp3.MP3Decoder(open("/mp3/new.mp3", "rb"))

audio.play(decoder)
while audio.playing:
    pass

print("Done playing!")
