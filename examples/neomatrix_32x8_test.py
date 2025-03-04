# SPDX-FileCopyrightText: 2025 Michael Doerr
# SPDX-FileCopyrightText: 2020 Melissa LeBlanc-Williams, written for Adafruit Industries
# SPDX-License-Identifier: MIT
"""
This example runs on a WaveShare ESP32-S3-Zero
"""

import board
import neopixel

import neomatrix

# Pin for my WaveShare ESP32-S3-Zero
pixel_pin = board.IO1
pixel_width = 32
pixel_height = 8
tiles_X = 1
tiles_Y = 1

pixels = neopixel.NeoPixel(
    pixel_pin,
    pixel_width * pixel_height,
    brightness=0.1,
    auto_write=False,
)

matrixType = ( neomatrix.NEO_MATRIX_TOP + neomatrix.NEO_MATRIX_LEFT +
               neomatrix.NEO_MATRIX_COLUMNS + neomatrix.NEO_MATRIX_ZIGZAG )

matrix = neomatrix.NeoMatrix(
    pixels,
    pixel_width, pixel_height,
    tiles_X, tiles_Y,
    matrixType,
    rotation=0,
)

matrix.fill(0x000088)
matrix.pixel(2, 1, 0xFFFF00)
matrix.line(0, 0, pixel_width - 1, pixel_height - 1, 0x00FF00)
matrix.line(0, pixel_height - 1, pixel_width - 1, 0, 0x00FF00)
matrix.circle(pixel_width // 2 - 1, pixel_height // 2 - 1, 4, 0xFF0000)
matrix.rect(1, 2, 8, pixel_height - 3, 0xFF00FF)
matrix.display()

