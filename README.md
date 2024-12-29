# Speed3

## Notes
---

## Mini Displays
Parts:
- [Blue 2.8in Oled Newhaven Display](https://newhavendisplay.com/2-8-inch-blue-graphic-oled-module/)
- [Sparkfun 8ch Level Shifter](https://www.sparkfun.com/products/19626)
  - TI TXS0108E breakout board
- Testing w/ Arduino nano
---
### 2.8in NHD info
- Default orientation: Top of display = pins at bottom
  - `u8g2.setDisplayRotation(U8G2_R2)` will rotate 180 / pins at top
- Display coords (?) (@ orientation 0) 
  - Box 0, 0, 0, 0:
    - 0-256 Left horizontal line start/end
    - 0-64 Top verticle line start/end
    - 0-256 Right horizontal line start/end
    - 0-64 Bottom verticle line start/end
  - Text 0, 0
    - 0-255 Depends on string length (~42 char)
    - Default font starts getting cut off at 6 so... 7-64
  - Circle (weird)
    - min: x 0, y 0, rad 0 is one pixel in the top left corner
    -
