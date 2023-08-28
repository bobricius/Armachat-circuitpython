import board
import time
from picomputer import *
import adafruit_imageload

player_loc = {"x": 100, "y": 100}

# Load the sprite sheet (bitmap)
sprite_sheet, paletteS = adafruit_imageload.load(
    "tilegame_assets/princess16.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette,
)
town_sheet, paletteT = adafruit_imageload.load(
    "tilegame_assets/town.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette,
)

# make the color at 0 index transparent.
paletteS.make_transparent(15)
paletteT.make_transparent(255)
# Create the sprite TileGrid
sprite = displayio.TileGrid(
    sprite_sheet,
    pixel_shader=paletteS,
    width=1,
    height=1,
    tile_width=64,
    tile_height=64,
    default_tile=0,
)

# Create the castle TileGrid
castle = displayio.TileGrid(
    town_sheet,
    pixel_shader=paletteT,
    width=20,
    height=7,
    tile_width=32,
    tile_height=32,
)

# Create a Group to hold the sprite and add it
sprite_group = displayio.Group()
sprite_group.append(sprite)

# Create a Group to hold the castle and add it
castle_group = displayio.Group(scale=1)
castle_group.append(castle)

# Create a Group to hold the sprite and castle
group = displayio.Group()

# Add the sprite and castle to the group
group.append(castle_group)
group.append(sprite_group)


# floor
idx=0
for y in range(0, 5):
    for x in range(0, 8):
        castle[x, y] = idx  # floor
        idx=idx+1

# put the sprite somewhere in the castle
sprite.x = player_loc["x"]
sprite.y = player_loc["y"]

# Add the Group to the Display
display.show(group)

floor=0
rotate=0
while True:
    keys=getKey(0)
    if keys:
        if keys == "lt":
            player_loc["x"] = max(0, player_loc["x"] - 1)
            rotate=1
        if keys == "rt":
            player_loc["x"] = min(320-64, player_loc["x"] + 1)
            rotate=3
        if keys == "up":
            player_loc["y"] = max(0, player_loc["y"] - 1)
            rotate=0
        if keys == "dn":
            player_loc["y"] = min(240-64, player_loc["y"] + 1)
            rotate=2
            
        if keys == "ent":
            for a in range(0, 7):
                sprite[0]=33+a
                time.sleep(0.2)
            rotate=3
            
#             for x in range(0, 19):
#                 for y in range(0, 7):
#                     castle[x, y] = floor  # floor
#             floor = floor +1

    # update the the player sprite position
    sprite.x = player_loc["x"]
    sprite.y = player_loc["y"]
    spra = player_loc["x"]+player_loc["y"]
    sprite[0]=(8*rotate)+spra%8
    time.sleep(0.01)

