# SPDX-FileCopyrightText: 2025 Mike Doerr
# SPDX-License-Identifier: MIT
'''
# Random walk on 16x16 neopixel matrix
'''

import board
import random
import time

import rainbowio
import matrix16

NEO_PIN = board.IO1     # for my WS ESP32-S3-Zero

matrix = matrix16.MatrixSetup(NEO_PIN, "hsquare", 0.1)

######

WIDTH = matrix._width
HEIGHT = matrix._height

X = WIDTH  // 2
Y = HEIGHT // 2

COL = 0
LEN = 5

def draw():
    global X, Y, COL, LEN

    nextX = X + random.randint(-LEN, LEN)
    if nextX<0: nextX = 0
    if nextX >= WIDTH: nextX = WIDTH-1

    nextY = Y + random.randint(-LEN, LEN)
    if nextY<0: nextY = 0
    if nextY >= HEIGHT: nextY = HEIGHT-1

    color = rainbowio.colorwheel(COL)
    matrix.line(X, Y, nextX, nextY, color)

    COL = (COL + random.randint(1, 9)) & 255
    X = nextX
    Y = nextY

def loop(count):
    matrix.fill(0)
    for i in range(count):
        draw()
        matrix.display()

CNT = 128
while True:
    loop(CNT)
    time.sleep(3)

