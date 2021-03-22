# Consolidating the Macro Keyboard logic
# into a tighter more concise package

import json
from CPButtonParser import parseButtons
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.consumer_control import ConsumerControl
import time
from ButtonPageUI import ButtonPageUI
from ButtonListUI import ButtonListUI

class M2PicoMacro:
    sysKeyActions={
    'key1':'showlist', #shows the list page
    'key2':'flipback', #Cycle to previous page
    'key3':'showlist',
    'key4':'flip' #Cycle to next page 
    }

    listKeyActions={
        'key1':'up',
        'key2':'down',
        'key3':'select',
        'key4':'select'
    }

    # ui = ButtonPageUI object
    def __init__(self,display):

        self._display=display
        #read json button defs
        f=open("/buttons.json")
        # load buttons pages
        self.buttonPages=json.load(f)
        f.close()

        for buttonPage in self.buttonPages["buttons"]:
            print("Button Page : %s"%(buttonPage["name"]))
            parseButtons(buttonPage)
       
        self.currButtonPageIndex=0
    
        #setup keyboard device
        self.keyboard=Keyboard(usb_hid.devices)
        self.cc=ConsumerControl(usb_hid.devices)

        #init button ui
        self.ui=ButtonPageUI()        

        #init list ui
        self.uilist=ButtonListUI(self.buttonPages["buttons"])
        self.listVisible=False

        #Initialize first button page
        self.LoadButtonPage(0)
        
        self._display.show(self.ui.group)


    # Loads the button page specified by the index
    def LoadButtonPage(self,newButtonPageIndex):
        self.currButtonDef=self.buttonPages["buttons"][newButtonPageIndex]        
        self.ui.LoadButtonPage(self.CurrentButtons)
        #print("Loaded Button Page - %s"%(self.currButtonDef["name"]))
    
    #Flip the button page index
    def FlipButtonPage(self,changeIndex,changePage=True):
        self.currButtonPageIndex+=changeIndex
        if self.currButtonPageIndex < 0:
            self.currButtonPageIndex=len(self.buttonPages['buttons'])-1
        elif self.currButtonPageIndex>=len(self.buttonPages['buttons']):
            self.currButtonPageIndex=0
        if changePage==True:    
            self.LoadButtonPage(self.currButtonPageIndex)
    

    #Button pressed down
    def ButtonDown(self,keyIndex):
        self.ui.SetButtonState(keyIndex,True)
        pass

    #Button released
    def ButtonUp(self,keyIndex):
        self.ui.SetButtonState(keyIndex,False)
        pass

    # Button presed on current page
    def ButtonPressed(self,keyIndex):
        if self.listVisible==True:
            self.ListButtonPressed(keyIndex)
        else:
            button = self.currButtonDef.get(keyIndex,None)
            if button != None and button['keycodes'] != None:
                print(keyIndex + "pressed")
                if(button["isCC"])==False:                
                    self.keyboard.send(*button['keycodes'])
                    time.sleep(150/1000)
                else:
                    self.cc.send(button["keycodes"][0])
    
    # Button pressed in list mode
    def ListButtonPressed(self,keyIndex):
        listAction=self.listKeyActions[keyIndex]
        self._display.auto_refresh=False
        if listAction=='up':
            self.FlipButtonPage(-1,False)
            self.uilist.setActiveItem(self.currButtonPageIndex)
        elif listAction=='down':
            self.FlipButtonPage(1,False)
            self.uilist.setActiveItem(self.currButtonPageIndex)
        elif listAction=="select":
            self.LoadButtonPage(self.currButtonPageIndex)
            self._display.show(self.ui.group)
            self.listVisible=False
        self._display.auto_refresh=True
        time.sleep(50/1000)

    #Long press of a button
    def ButtonLongPressed(self,keyIndex):
        sysaction=self.sysKeyActions[keyIndex]
        print("Sys Key action :" + sysaction)
        self._display.auto_refresh=False
        if sysaction=='flip':
            self.FlipButtonPage(1)
            
        elif sysaction=='flipback':
            self.FlipButtonPage(-1)
            
        elif sysaction=="showlist":
            #show page list
            self.uilist.setActiveItem(self.currButtonPageIndex)
            self._display.show(self.uilist.group)
            self.listVisible=True
        self._display.auto_refresh=True
        time.sleep(150/1000)
        

    #Current Page Dictionary
    @property
    def CurrentButtons(self):
        return self.currButtonDef
    