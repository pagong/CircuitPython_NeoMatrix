# SPDX-FileCopyrightText: 2024 Tim Cocks for Adafruit Industries
# SPDX-FileCopyrightText: 2024 Michael Doerr
#
# SPDX-License-Identifier: MIT
import board
import neopixel

import neomatrix

from snake.animate_snake import SnakeAnimation

# Update to match the pin connected to your NeoPixels
pixel_pin = board.IO1
# Update to match the number of NeoPixels you have connected
pixel_num = 256

BRIGHT=0.05
# initialize the neopixels. Change out for dotstars if needed.
pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=BRIGHT, auto_write=False)


matrixType = ( neomatrix.NEO_MATRIX_BOTTOM + neomatrix.NEO_MATRIX_LEFT +
               neomatrix.NEO_MATRIX_ROWS + neomatrix.NEO_MATRIX_ZIGZAG )

matrix = neomatrix.NeoMatrix(pixels, 16, 16, 1, 1, matrixType)


# initialize the animation
snake = SnakeAnimation(matrix, speed=0.1, color=0xff00ff, snake_length=5)

while True:
    # call animation to show the next animation frame
    snake.animate()

