import displayio
import terminalio
from adafruit_display_text import label
from adafruit_button import Button

#Index the string to a button position
KEYMAP={
    'key1':0,
    'key2':1,
    'key3':2,
    'key4':3
    }
#How high the TITLE is
TITLE_HEIGHT=15
# This defines the actual UI page
class ButtonPageUI():
    # display = Display object
    def __init__(self):

        
        # Pretty sure this isn't the right way to do this
        # should be inherited from group instead
        self._group = displayio.Group(max_size=30)
        
        # This is the group used to hold the button page
        self._groupPage = displayio.Group(max_size=30)        
        self._group.append(self._groupPage)
        self._groupPage.hidden=True
        # Create the title
        self._title=label.Label(terminalio.FONT,text="title",max_glyphs=35)
        self._title.anchor_point=(0.5,0.5)        
        self._title.anchored_position=(240/2,TITLE_HEIGHT/2)
        # self._group.append(self._title)
        self._groupPage.append(self._title)

        #Initialize the buttons
        self._buttons=[]
        #Interestingly, initialize it like this
        #indexes the buttons the same as the KEYS
        #itself...
        for x in range(2):
            for y in range(2):
                button=Button(x=120*x,
                      y=TITLE_HEIGHT+(60*y),
                      width=120,
                      height=60,
                      style=Button.ROUNDRECT,
                      outline_color=0xff0000,
                      fill_color=None,
                      label_color=0x00ff00,
                      label_font=terminalio.FONT,
                      label="Button " + str(len(self._buttons)),
                      selected_fill=0x00ff00)
                self._buttons.append(button)
                self._groupPage.append(button)
                
                
    #Returns the display group surface
    @property
    def group(self):
        return self._group
    

    def SetButtonState(self,buttonkey,selected):
        self._buttons[KEYMAP[buttonkey]].selected=selected
        
    # Based on the JSON button page
    # customize the UI
    def LoadButtonPage(self,dictPage):
        #parse color if present
        strColor=dictPage.get("color")
        if strColor==None:
            pageColor=0xa0a0a0
        else:
            pageColor=int(strColor,16)

        self._title.text=dictPage["name"]
        self._title.color=pageColor
        for i in KEYMAP.keys():    
            print("Key Map: " + i)
            buttondef=dictPage.get(i)
            button=self._buttons[KEYMAP[i]]
            if buttondef==None:
                print("Hidding Button " + str(KEYMAP[i]))
                button.label="-"
            else:                
                button.label=dictPage[i]["caption"]
            button.outline_color=pageColor
            button.label_color=pageColor
            button.selected_fill=pageColor

    def ShowPageList(self):
        self._group.remove(self._groupPage)
        
