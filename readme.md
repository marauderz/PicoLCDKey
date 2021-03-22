# Pico Shortcut Key Gadget

This here is a Circuit Python program which can be uses on a **Raspberry Pi Pico** and a **Waveshare Pico LCD** attached on it to create a simple shortcut key gadget, basically something that presses keys when one of the buttons are pressed.

- Raspberry Pi Pico - https://www.raspberrypi.org/products/raspberry-pi-pico/
- WaveShare Pico LCD - https://www.waveshare.com/pico-lcd-1.14.htm

## Dependent Libraries
List of Circuit Python libraries which are needed from the additional libraries bundle
- adafruit_display_shapes
- adafruit_display_text
- adafruit_hid
- adafruit_button.mpy
- adafruit_st7789.mpy

## Usage

If you have all the hardware ready, you can just dump the contents of **dist** on a Raspberry Pico with CircuitPython installed and it should just run.

Pressing the button on the screen will send the keypresses to the connected device. Note that the Key names start from 1 in the buttons.json file instead of 0... Because I was too lazy to change the code from it's Raspbery Pi incarnation. 😝

Holding **Key1** or **Key3** on the LCD for 1 second will move between the pages of buttons.

Holding **Key0** on the LCD will bring you to a list of the button pages to make it easier to switch if you have a lot of buttons.Then Use **Key0** and **Key1** to move up and down the list, **Key2** and **Key3** to select the highlighted page.

## buttons.json

The **buttons.json** file used to define the buttons is pretty self explanatory. Just note that the names for the keys needs to be the same as what you see here (https://github.com/adafruit/Adafruit_CircuitPython_HID/blob/master/adafruit_hid/keycode.py) 

In order to access media controls (ie. Volume up, down, etc.). Make sure the button is defined with a **type="cc"** value. You can only have ONE keycode in a Consumer Control button, and use the keycodes from here (https://github.com/adafruit/Adafruit_CircuitPython_HID/blob/master/adafruit_hid/consumer_control_code.py)

## Final Notes
This is my first real project with Python and Microcontrollers, so I'm gonna think the code isn't particularly pretty, most importantly the code for handling the actual buttons.

I decided to upload this code because WaveShare themselves didn't have any Python samples for their Pico LCD at the time of writing. (March 2nd 2021)