# Simple code to initialize the WaveShare PicoLCD
# and return the Circuit Python ST7789 object
import board
import displayio
import busio 
import time
from adafruit_display_text import label
from adafruit_st7789 import ST7789

# Define some constants related to the keys
class PicoKey:
    KEY0=board.GP15
    KEY1=board.GP17
    KEY2=board.GP2
    KEY3=board.GP3
    # Pressed State
    # I don't know why the switch
    # reports FALSE on pressed.
    PRESSED=False

def InitWSPicoLCD():
    spi = busio.SPI(clock=board.GP10,MOSI=board.GP11)

    tft_cs = board.GP9
    tft_dc = board.GP8
    tft_reset = board.GP12
    display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs,reset=tft_reset)
    
    # How do we know what's the correct value for rowstart and colstart?
    display = ST7789(
        display_bus, rotation=270, width=240, height=135, rowstart=40, colstart=53
    )
    return display