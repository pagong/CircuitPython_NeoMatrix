## CircuitPython_NeoMatrix

Port of Adafruit's `Adafruit_NeoMatrix` [library][ada01] for the Arduino to CircuitPython.  
See the [Adafruit NeoPixel Überguide][ada02] for everything you need to know about NeoPixel grids.

- Features:
  - Single matrix: 8x8, 16x16, 8x32, 32x8 NeoPixels
  - Tiled matrices: multiple single matrices

### Single matrix
- Horizontal strips (row major)
  - 8w * 8h, 16w * 16h , 8w * 32h
  - zigzag and progressive rows
- Vertical strips (column major)
  - 8w * 8h, 16w * 16h, 32w * 8h
  - zigzag and progressive columns
- Position of first Pixel
  - Bottom, Top, Left, Right

### Tiled matrices
- Assumption: only identical matrices are used
  - tiles of size 8 * 8, or 16 * 16, or 8 * 32, or 32 * 8
- Tiles are laid out in a regular style
  - N * tiles in X direction, either Left --> Right, or reversed
  - M * tiles in Y direction, either Top --> Down, or reversed
  - tiles are wired either in progressive or zigzag mode
- Position of first Tile
  - Bottom, Top, Left, Right


## Basic Usage
1. Determine size and led arrangement of a single NeoPixel matrix.
2. Determine number and tile arrangement of your NeoPixel matrices.
3. Use these values to compute a `matrixType` variable and several size values.
4. Create a normal CircuitPython `neopixel.NeoPixel` object.
5. Use this `NeoPixel` object, the `matrixType` variable, and size values to create a `neomatrix.NeoMatrix` object.
6. Finally, use the APIs of the `NeoMatrix` object to draw colorful animations using X and Y coordinates.


## Advanced Usage
A `NeoMatrix` object is made from a `NeoPixel` [strip][ada03], a `FrameBuffer` [object][ada04],
and from a `PixelGrid` [object][ada08]. That's why several APIs can be used to change the color of NeoPixels.

### NeoMatrix FrameBuffer API
This drawing API is based on the `adafruit_pixel_framebuf` [library][ada06] by Melissa LeBlanc-Williams.
However, it is extended from one matrix to an array of matrix tiles.

### NeoGrid PixelMap API
This drawing API is based on the `adafruit_led_animation.grid` [library][ada08] by Kattni Rembor.
However, it is extended from one matrix to an array of matrix tiles.


## Demos

The `examples` directory has several demos that are showing how the
`neomatrix.py` library and the helper modules `matrix<##>.py` can be used.

Python files with an 8 in the name are intended for 8x8 or 8x32 NeoPixel matrices.
Files with a 16 in the name are meant for 16x16 NeoMatrices and 
files with a 32 in the name should be used for tiled 32x32 matrices.

``` bash
examples/
├── berlin          # "Berlin-Uhr"
├── bounce          # bouncing lines and random walks
├── rainbow         # spiraling rainbows
├── life            # Tim C's Game of Life animation
├── snake           # Tim C's snake animation
├── fire            # Mark Kriegsman's Fire2012 simulation
├── water           # Waterfall (Fire2012 with a blue palette)
└── snoise          # Simplex Noise demo using Tod Kurt's library
```

---

[ada01]: https://github.com/adafruit/Adafruit_NeoMatrix
[ada02]: https://learn.adafruit.com/adafruit-neopixel-uberguide/neomatrix-library

[ada03]: https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel
[ada04]: https://github.com/adafruit/Adafruit_CircuitPython_framebuf
[ada05]: https://github.com/adafruit/Adafruit_CircuitPython_PixelMap

[ada06]: https://github.com/adafruit/Adafruit_CircuitPython_Pixel_Framebuf
[ada07]: https://github.com/adafruit/Adafruit_CircuitPython_LED_Animation
[ada08]: https://github.com/adafruit/Adafruit_CircuitPython_LED_Animation/blob/main/adafruit_led_animation/grid.py
[ada09]: https://github.com/adafruit/Adafruit_CircuitPython_LED_Animation/blob/main/adafruit_led_animation/helper.py

