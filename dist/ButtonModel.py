import json
from CPButtonParser import parseButtons
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.consumer_control import ConsumerControl
import time

# model for the button dataset
class ButtonModel:
    def __init__(self):
        #read json button defs
        f=open("/buttons.json")
        # load buttons pages
        self.buttonPages=json.load(f)
        f.close()

        for buttonPage in self.buttonPages["buttons"]:
            print("Button Page : %s"%(buttonPage["name"]))
            parseButtons(buttonPage)
        self.LoadButtonPage(0)
        self.currButtonPageIndex=0
        
        #setup keyboard device
        self.keyboard=Keyboard(usb_hid.devices)
        self.cc=ConsumerControl(usb_hid.devices)

    # Loads the button page specified by the index
    def LoadButtonPage(self,newButtonPageIndex):
        self.currButtonDef=self.buttonPages["buttons"][newButtonPageIndex]
        #print("Changeing BGImg To " + buttonDef['img'] )
        #imgbg=Image.open(buttonDef['img'])
        print("Loaded Button Page - %s"%(self.currButtonDef["name"]))
    
    #Flip the button page index
    def FlipButtonPage(self,changeIndex):
        self.currButtonPageIndex+=changeIndex
        if self.currButtonPageIndex < 0:
            self.currButtonPageIndex=len(self.buttonPages['buttons'])-1
        elif self.currButtonPageIndex>=len(self.buttonPages['buttons']):
            self.currButtonPageIndex=0    
        self.LoadButtonPage(self.currButtonPageIndex)
    
    # Button presed on current page
    def ButtonPressed(self,keyIndex):
        button = self.currButtonDef.get(keyIndex,None)
        if button != None and button['keycodes'] != None:
            print(keyIndex + "pressed")
            if(button["isCC"])==False:                
                self.keyboard.send(*button['keycodes'])
                time.sleep(150/1000)
            else:
                self.cc.send(button["keycodes"][0])
        
    #Current Page Dictionary
    @property
    def CurrentButtons(self):
        return self.currButtonDef
    
