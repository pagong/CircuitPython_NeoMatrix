# noise_square_code.py -- playing with simplex noise in CircuitPython
# 9 Feb 2023 - @todbot / Tod Kurt
# https://github.com/todbot/CircuitPython_Noise
#
# 2 Mar 2025 - @pagong
# Uses WaveShare ESP32-S3-Matrix with an 8x8 LED matrix
# https://circuitpython.org/board/waveshare_esp32_s3_matrix/

import time
import board
import random
import neopixel
import rainbowio

#####################

# for WS ESP32-S3-Matrix with 8x8 NeoPixel-Matrix
NUM_COLS = 8
NUM_CELLS = 8

NUM_PIXELS = (NUM_COLS * NUM_CELLS)  # Update this to match the number of LEDs.
SPEED = 0.01       # Increase to slow down the animation. Decrease to speed it up.
BRIGHTNESS = 0.1   # A number between 0.0 and 1.0, where 0.0 is off, and 1.0 is max.
PIN = board.IO14   # This is the default pin on WS ESP32-S3-Matrix with 8x8 NeoPixel matrix

leds = neopixel.NeoPixel(PIN, NUM_PIXELS, brightness=BRIGHTNESS,
                         pixel_order=neopixel.RGB, auto_write=False)

# prepare rainbow palette
palette = []
for k in range(256):
    palette.append(rainbowio.colorwheel(k))


# use Todbot's noise module from community bundle
import noise
noise_scale = 0.07   # noise_scale * max(width, height) should be smaller than 1.0
noise_incr = 0.01
noise_x = 0.0
noise_y = 0.0
xsign = 0.0
ysign = 1.0

#####################

# change direction of movement
def change_direction():
    xs, ys = 0, 0
    while (abs(xs) + abs(ys) == 0):
        xs = random.randint(-1, 1)
        ys = random.randint(-1, 1)
    return float(xs), float(ys)

def do_frame():
    for i in range(NUM_COLS):       # for each pixel column
        for j in range(NUM_CELLS):  # for each pixel row
            index = j*NUM_COLS + i
            # get a noise value in 2D noise space
            n = noise.noise( noise_x + noise_scale*i, noise_y + noise_scale*j )
            # Original:
            # c = int((n+1) * 255)           # scale it from -1 - +1 -> 0 - 510
            # Bugfix:
            c = int((n+1.0) * 127.5)         # scale it from -1 - +1 -> 0 - 255
            leds[index] = palette[c & 255]   # convert to hue

#####################

Debug = True

while True:
    t1 = time.monotonic_ns()
    do_frame()
    t2 = time.monotonic_ns()

    leds.show()
    t3 = time.monotonic_ns()

    if Debug:
        d1 = (t2 - t1) / 1000000.0
        print(f"Compute {d1} ms", end=" +\t")
        d2 = (t3 - t2) / 1000000.0
        print(f"Display {d2} ms", end=" =\t")
        print(f"Total {d1+d2} ms", end=" -->\t")
        print(f"{1000.0/(d1+d2)} fps")

    # move around in noise space
    noise_x += noise_incr * xsign
    noise_y += noise_incr * ysign
    if (random.randint(0, 99) == 8):
        xsign, ysign = change_direction()

    time.sleep(SPEED)

