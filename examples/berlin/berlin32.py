# SPDX-FileCopyrightText: 2025-2026 Mike Doerr
# SPDX-License-Identifier: MIT

import time
import board
import os
import rtc

import wifi
import socketpool
import ssl
import adafruit_ntp
import adafruit_requests

import neopixel
import neomatrix

from matrix32 import MatrixSetup

#######################################

NUM_COLS = 16
NUM_CELLS = 16
NUM_PIXEL = (NUM_COLS * NUM_CELLS)

BRIGHTNESS = 0.1
SLEEP = 0.1

# NEO_PIN is for WaveShare ESP32-S3-Zero
NEO_PIN = board.IO1

# NEO_PIN is for Pico-W
#NEO_PIN = board.GP28

matrix = MatrixSetup(NEO_PIN, "vstripes", 0.1)

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
BLUE    = 0x0000FF

# unused colors
WHITE   = 0xFFFFFF
GREEN   = 0x00FF00
CYAN    = 0x00C0C0
MAGENTA = 0xC000C0

#######################################

# Layout of rectangles of Berlin-Uhr
xoff = 1
yoff = 5

a = 2
b = 2
c = 6
d = 4
e = 1

# Four 6x4 rects for hour*5
x = xoff
y = yoff+2*b
hour5 = [ (x, y, c, d),
          (x+b+c, y, c, d),
          (x+2*b+2*c, y, c, d),
          (x+3*b+3*c, y, c, d) ]

# Four 6x4 rects for hour*1
x = xoff
y = yoff+3*b+d
hour1 = [ (x, y, c, d),
          (x+b+c, y, c, d),
          (x+2*b+2*c, y, c, d),
          (x+3*b+3*c, y, c, d) ]

# Eleven 2x4 rects for minutes*5
x = 0
y = yoff+3*b+2*d+b+e
minute5 = [ (x, y, a, d),
            (x+a+e, y, a, d),
            (x+2*a+2*e, y, a, d),
            (x+3*a+3*e, y, a, d),
            (x+4*a+4*e, y, a, d),
            (x+5*a+5*e, y, a, d),
            (x+6*a+6*e, y, a, d),
            (x+7*a+7*e, y, a, d),
            (x+8*a+8*e, y, a, d),
            (x+9*a+9*e, y, a, d),
            (x+10*a+10*e, y, a, d) ]

# Four 6x4 rects for minutes*1
x = xoff
y = yoff+4*b+3*d+b+e
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
        grid.fill_rect(rect[0], rect[1], rect[2], rect[3], color)

    h1 = hour%5
    for i in range(4):
        rect = hour1[i]
        color = ORANGE if (i < h1) else GREY
        grid.fill_rect(rect[0], rect[1], rect[2], rect[3], color)


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
        grid.fill_rect(rect[0], rect[1], rect[2], rect[3], color)


def Draw_seconds(grid, second, color):
    # blink the circle at the top
    x = 15 ; y = 1 ; l = 2
    grid.hline(x,   y,   l,   color)
    grid.hline(x-1, y+1, l+2, color)
    grid.hline(x-2, y+2, l+4, color)
    grid.hline(x-2, y+3, l+4, color)
    grid.hline(x-1, y+4, l+2, color)
    grid.hline(x,   y+5, l,   color)
    # show a bar in the middle
    barlen = 1 + second // 2
    y = yoff+3*b+2*d+e
    grid.hline(1, y, barlen, BLUE)
    
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
        matrix.fill(BLACK)

        Draw_minutes(matrix, minute)
        Draw_hours(matrix, hour)

    if second != last_sec:
        last_sec = second
        # blink second mark
        color = LIME if (second & 1) else GREY
        Draw_seconds(matrix, second, color)

        # show the matrix
        matrix.display()

    time.sleep(SLEEP)

