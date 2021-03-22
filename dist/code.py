import board
import time
import digitalio
import displayio
from CPButtonParser import parseButtons
from picolcd import InitWSPicoLCD,PicoKey
from ButtonPageUI import ButtonPageUI
from M2PicoMacro import M2PicoMacro

#Initialize the LCD
displayio.release_displays()
display=InitWSPicoLCD()

# our pico key object
picoKey=M2PicoMacro(display)

#define our pins
dPins={
    'key1':digitalio.DigitalInOut(PicoKey.KEY0),    
    'key2':digitalio.DigitalInOut(PicoKey.KEY1),
    'key3':digitalio.DigitalInOut(PicoKey.KEY2),     
    'key4':digitalio.DigitalInOut(PicoKey.KEY3)
}

# Setup a dict to track syspin key down states
PinStates={}
for key in dPins:
    PinStates[key]=0
    
#quick way to setup up the pins to pull down
def PinSetup(dPins):
    for key in dPins:
        pin=dPins[key]
        pin.switch_to_input(pull=digitalio.Pull.DOWN)
PinSetup(dPins)

while True:
    for key in dPins:
        pinRead=dPins[key]
        sysTiming=PinStates[key]
        if pinRead.value==PicoKey.PRESSED:
            if sysTiming==0:
                # Start tracking when button was
                # pressed
                PinStates[key]=time.monotonic()
                picoKey.ButtonDown(key)
            elif sysTiming>0 and (time.monotonic() - sysTiming) > 1:
                # Key held down longer than 1 seconds
                # mark key as processed
                picoKey.ButtonUp(key)
                PinStates[key]=-1
                picoKey.ButtonLongPressed(key)
        else:
            if sysTiming>0:
                # Button was released without holding
                # longer than 1 sec, do normal key processing
                PinStates[key]=0
                picoKey.ButtonUp(key)
                picoKey.ButtonPressed(key)
            elif sysTiming<0:
                # Button released after sys key action
                # reset for next check
                PinStates[key]=0
    pass
                