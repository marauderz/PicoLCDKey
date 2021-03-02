import board
import terminalio
import displayio
import time
from adafruit_display_text import label
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_button import Button
import digitalio
import json
from CPButtonParser import parseButtons
from picolcd import InitWSPicoLCD,PicoKey
from ButtonPageUI import ButtonPageUI
from ButtonModel import ButtonModel

#Initialize the LCD
displayio.release_displays()
display=InitWSPicoLCD()

buttonUI=ButtonPageUI()
buttonModel=ButtonModel()

buttonUI.LoadButtonPage(buttonModel.CurrentButtons)

display.show(buttonUI.group)

#Normal Pins, respond immediately when pressed
dPins={
    'key1':digitalio.DigitalInOut(PicoKey.KEY0),    
    'key3':digitalio.DigitalInOut(PicoKey.KEY2),
}

#System Pins, release before 1 second will perform
#normal function, held longer they'll perform 
#other commands
sysPins={
    'key2':digitalio.DigitalInOut(PicoKey.KEY1),
    'key4':digitalio.DigitalInOut(PicoKey.KEY3)
}
#Determine what action a sys key performs
sysKeyActions={
    'key4':'flip', #Cycle to next page
    'key2':'flipback' #Cycle to previous page
}
# Setup a dict to track syspin key down states
PinStates={}
for key in sysPins:
    PinStates[key]=0

for key in dPins:
    PinStates[key]=0
    

#quick way to setup up the pins to pull down
def PinSetup(dPins):
    for key in dPins:
        pin=dPins[key]
        pin.switch_to_input(pull=digitalio.Pull.DOWN)
PinSetup(dPins)
PinSetup(sysPins)

# Key was pressed, providing keyindex
def keyPressed(keyIndex):
    buttonModel.ButtonPressed(keyIndex)
    

def sysKeyAction(keyIndex):
    sysaction=sysKeyActions[keyIndex]
    print("Sys Key action :" + sysaction)
    display.auto_refresh=False
    if sysaction=='flip':
        buttonModel.FlipButtonPage(1)
        buttonUI.LoadButtonPage(buttonModel.CurrentButtons)
    elif sysaction=='flipback':
        buttonModel.FlipButtonPage(-1)
        buttonUI.LoadButtonPage(buttonModel.CurrentButtons)
    display.auto_refresh=True
    time.sleep(150/1000)


while True:
    for key in dPins:
        pinRead=dPins[key]
        pinTiming=PinStates[key]
        if pinRead.value==PicoKey.PRESSED:
            if pinTiming==0:
                keyPressed(key)
                buttonUI.SetButtonState(key,True)
                PinStates[key]=time.monotonic()
        else:
            if pinTiming > 0:
                buttonUI.SetButtonState(key,False)
                PinStates[key]=0
    for key in sysPins:
        pinRead=sysPins[key]
        sysTiming=PinStates[key]
        if pinRead.value==PicoKey.PRESSED:
            if sysTiming==0:
                # Start tracking when button was
                # pressed
                PinStates[key]=time.monotonic()
                buttonUI.SetButtonState(key,True)
            elif sysTiming>0 and (time.monotonic() - sysTiming) > 1:
                # Key held down longer than 1 seconds
                # mark key as processed
                buttonUI.SetButtonState(key,False)
                PinStates[key]=-1
                sysKeyAction(key)
        else:
            if sysTiming>0:
                # Button was released without holding
                # longer than 1 sec, do normal key processing
                PinStates[key]=0
                buttonUI.SetButtonState(key,False)
                keyPressed(key)
            elif sysTiming<0:
                # Button released after sys key action
                # reset for next check
                PinStates[key]=0
                
    time.sleep(10/1000)


