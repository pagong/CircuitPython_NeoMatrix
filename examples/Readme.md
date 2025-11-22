## Demos

The `examples` directory has several demos that are showing how the
`neomatrix.py` library and the helper modules `matrix<##>.py` can be used.

Python files with an 8 in the name are intended for 8x8 or 8x32 NeoPixel matrices.  
Files with a 16 in the name are meant for 16x16 NeoMatrices and   
files with a 32 in the name should be used for tiled 32x32 matrices.

``` bash
examples/
├── berlin              # "Berlin-Uhr": digital clock with a twist
│   └── berlin16.py
├── bounce              # bouncing lines and random walks
│   ├── bounce32.py
│   ├── lines16.py
│   ├── lines32.py
│   ├── point.py
│   ├── walk16.py
│   └── walk32.py
├── rainbow             # spiraling rainbows
│   ├── spiral16_a.py
│   ├── spiral16_b.py
│   ├── spiral16_c.py
│   ├── spiral32_a.py
│   ├── spiral32_b.py
│   ├── spiral8_a.py
│   └── spiral8_b.py
├── life                # Tim C's Game of Life animation
│   ├── animate_life.py
│   ├── life16.py
│   ├── life32.py
│   └── life8.py
├── snake               # Tim C's snake animation
│   ├── animate_snake.py
│   ├── snake16.py
│   ├── snake32.py
│   └── snake8.py
├── fire                # Mark Kriegsman's Fire2012 simulation
│   ├── fire16_a.py
│   ├── fire16_b.py
│   ├── fire16_c.py
│   ├── fire32.py
│   ├── fire8_a.py
│   └── fire8_b.py
├── water               # Waterfall (Fire2012 with a blue palette)
│   ├── water16_a.py
│   ├── water16_b.py
│   ├── water16_c.py
│   ├── water32.py
│   ├── water8_a.py
│   └── water8_b.py
└── snoise              # Simplex Noise demo using Tod Kurt's library
    ├── noise16a.py
    ├── noise16b.py
    ├── noise16c.py
    ├── noise16d.py
    ├── noise32a.py
    ├── noise32b.py
    ├── noise32c.py
    ├── noise32d.py
    ├── noise32e.py
    ├── noise8a.py
    ├── noise8b.py
    └── noise8c.py
```

