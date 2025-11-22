# SPDX-FileCopyrightText: 2025 Mike Doerr
# SPDX-License-Identifier: MIT

import time
import board
import os
import rtc

import wifi
import socketpool
import ssl
#import ipaddress
import adafruit_ntp
import adafruit_requests

import neopixel
import neomatrix

#######################################

NUM_COLS = 16
NUM_CELLS = 16
NUM_PIXEL = (NUM_COLS * NUM_CELLS)

BRIGHTNESS = 0.1
SLEEP = 0.1

# NEO_PIN is for WaveShare ESP32-S3-Zero
NEO_PIN = board.IO1

# create and clear pixel buffer
pixels = neopixel.NeoPixel(
    NEO_PIN, NUM_PIXEL,
    brightness = BRIGHTNESS,
    auto_write = False
)
pixels.fill(0)

matrixType = (
    neomatrix.NEO_MATRIX_BOTTOM +
    neomatrix.NEO_MATRIX_LEFT +
    neomatrix.NEO_MATRIX_ROWS +
    neomatrix.NEO_MATRIX_ZIGZAG
)

# create the "16x16" grid 
grid = neomatrix.NeoMatrix(
        pixels,
        NUM_COLS, NUM_CELLS,
        1, 1,
        matrixType, rotation=0,
)

#######################################

TZ = os.getenv('TZ')
UTC_OFFSET = os.getenv('UTC_OFFSET')
# Wifi details are in settings.toml file
WLAN_SSID = os.getenv('CIRCUITPY_WIFI_SSID')
WLAN_PASS = os.getenv('CIRCUITPY_WIFI_PASSWORD')

print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])
print("Connecting to %s"%WLAN_SSID)

try:
#if True:
    wifi.radio.connect(WLAN_SSID, WLAN_PASS)
    pool = socketpool.SocketPool(wifi.radio)

    print("Connected to %s!"%WLAN_SSID)
    print("My IP address: ", wifi.radio.ipv4_address)

    if UTC_OFFSET is None:
        requests = adafruit_requests.Session(pool, ssl.create_default_context())
        response = requests.get("http://worldtimeapi.org/api/timezone/" + TZ)
        #print(response)
        response_as_json = response.json()
        UTC_OFFSET = response_as_json["raw_offset"] + response_as_json["dst_offset"]

    ntp = adafruit_ntp.NTP(pool, server="de.pool.ntp.org", tz_offset=UTC_OFFSET // 3600)
    dtm = ntp.datetime
except:
    dtm = time.struct_time( (2025, 11, 23,   23, 42, 0,    0, 0, 0) )

print(dtm)
rtc.RTC().datetime = dtm

#######################################

# define color names
RED     = 0xFF0000
YELLOW  = 0xC0C000
LIME    = 0x70C000
ORANGE  = 0xC07000
BLACK   = 0x000000
GREY    = 0x171717

# unused colors
WHITE   = 0xFFFFFF
GREEN   = 0x00FF00
BLUE    = 0x0000FF
CYAN    = 0x00C0C0
MAGENTA = 0xC000C0

#######################################

# Layout of rectangles of Berlin-Uhr
xoff = 2
yoff = 4

a = b = 1
c = d = 2

# Four 2x2 rects for hour*5
x = xoff
y = yoff
hour5 = [ (x, y, c, d),
          (x+b+c, y, c, d),
          (x+2*b+2*c, y, c, d),
          (x+3*b+3*c, y, c, d) ]

# Four 2x2 rects for hour*1
y = yoff+d+b
hour1 = [ (x, y, c, d),
          (x+b+c, y, c, d),
          (x+2*b+2*c, y, c, d),
          (x+3*b+3*c, y, c, d) ]

# Eleven 1x2 rects for minutes*5
y = yoff+2*d+2*b
minute5 = [ (x, y, a, d),
            (x+a, y, a, d),
            (x+2*a, y, a, d),
            (x+3*a, y, a, d),
            (x+4*a, y, a, d),
            (x+5*a, y, a, d),
            (x+6*a, y, a, d),
            (x+7*a, y, a, d),
            (x+8*a, y, a, d),
            (x+9*a, y, a, d),
            (x+10*a, y, a, d) ]

# Four 2x2 rects for minutes*1
y = yoff+3*d+3*b
minute1 = [ (x, y, c, d),
            (x+b+c, y, c, d),
            (x+2*b+2*c, y, c, d),
            (x+3*b+3*c, y, c, d) ]

#######################################

def Draw_hours(grid, hour):
    h5 = hour//5
    for i in range(4):
        rect = hour5[i]
        color = RED if (i < h5) else GREY
        grid.rect(rect[0], rect[1], rect[2], rect[3], color)

    h1 = hour%5
    for i in range(4):
        rect = hour1[i]
        color = ORANGE if (i < h1) else GREY
        grid.rect(rect[0], rect[1], rect[2], rect[3], color)


def Draw_minutes(grid, minute):
    m5 = minute//5
    for i in range(11):
        rect = minute5[i]
        color = RED if (i%3) == 2 else YELLOW
        if (i%3) == 1: color = ORANGE
        if (i >= m5): color = GREY
        grid.rect(rect[0], rect[1], rect[2], rect[3], color)

    m1 = minute%5
    for i in range(4):
        rect = minute1[i]
        color = YELLOW if (i < m1) else GREY
        grid.rect(rect[0], rect[1], rect[2], rect[3], color)


def Draw_second(grid, color):
    grid.pixel(7, 0, color)
    grid.hline(6, 1, 3, color)
    grid.pixel(7, 2, color)
    
#######################################

last_sec = -1
last_min = -1

# Main loop
while True:
    lt = time.localtime()

    hour   = lt.tm_hour
    minute = lt.tm_min
    second = lt.tm_sec

    # update berlin clock once per minute
    if minute != last_min:
        last_min = minute
        # clear the matrix
        grid.fill(BLACK)

        Draw_minutes(grid, minute)
        Draw_hours(grid, hour)

    if second != last_sec:
        last_sec = second
        # blink second mark
        color = LIME if (second & 1) else GREY
        Draw_second(grid, color)

        # show the matrix
        grid.display()

    time.sleep(SLEEP)

