from adafruit_slideshow import SlideShow

from picomputer import *


slideshow = SlideShow(
    display,
    None,
    folder="/bmps",
    loop=True,
    order=0,
    fade_effect=False,
    dwell=1,
    auto_advance=True,
)

slideshow.brightness=1
while slideshow.update():
    pass


