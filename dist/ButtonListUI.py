# This class handles the button list

import displayio
import terminalio
from adafruit_display_text import label
from adafruit_button import Button

class ButtonListUI:
    def __init__(self,pageList):
        self._group=displayio.Group(max_size=99)

        #Our button collection
        self.buttons=[]
        self.pageList=pageList

        btnUpper=Button(x=0,
            y=0,
            width=240,
            height=40,
            style=Button.ROUNDRECT,
            outline_color=0xdddddd,
            fill_color=None,
            label_color=0xdddddd,
            label_font=terminalio.FONT,
            label="TOP",
            selected_fill=0xdddddd)
        self.buttons.append(btnUpper)
        self._group.append(btnUpper)
        
        btnMid=Button(x=0,
            y=40,
            width=240,
            height=50,
            style=Button.ROUNDRECT,
            outline_color=0xdddddd,
            fill_color=None,
            label_color=0xdddddd,
            label_font=terminalio.FONT,
            label="MID",
            selected_fill=0xdddddd)
        btnMid.selected=True
        self.buttons.append(btnMid)
        self._group.append(btnMid)

        btnLow=Button(x=0,
            y=90,
            width=240,
            height=40,
            style=Button.ROUNDRECT,
            outline_color=0xdddddd,
            fill_color=None,
            label_color=0xdddddd,
            label_font=terminalio.FONT,
            label="LOW",
            selected_fill=0xdddddd)
        self.buttons.append(btnLow)
        self._group.append(btnLow)


    @property
    def group(self):
        return self._group

    # Given the page index, update the
    # buttons to show the selected page
    def setActiveItem(self,pageIndex):
        #Load the colors of the given page
        currPage=self.pageList[pageIndex]
        strColor=currPage.get("color")
        if strColor==None:
            pageColor=0xa0a0a0
        else:
            pageColor=int(strColor,16)
        pass


        # Top Button
        button=self.buttons[0]
        button.outline_color=pageColor
        button.label_color=pageColor
        button.selected_fill=pageColor
        if pageIndex==0:
            #prevbutton label is the last item on the
            #list to warp around
            button.label=self.pageList[len(self.pageList)-1].get("name")
        else:
            button.label=self.pageList[pageIndex-1].get("name")

        # Middle Button
        button=self.buttons[1]
        button.outline_color=pageColor
        button.label_color=(~pageColor) & 0xFFFFFF
        button.selected_fill=pageColor
        button.label=currPage.get("name")

        # Middle Button
        button=self.buttons[2]
        button.outline_color=pageColor        
        button.label_color=pageColor
        button.selected_fill=pageColor
        if pageIndex==len(self.pageList)-1:
            #next label is the first item on the list
            button.label=self.pageList[0].get("name")
        else:
            button.label=self.pageList[pageIndex+1].get("name")

        
