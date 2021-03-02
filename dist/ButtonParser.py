from keycodedef import KEYCODESLU

# Parses the button def
# files from the string
# defininition for keycodes
# into their numbers

def parseButtons(buttonDef):
    for i in buttonDef:
        # ignore things we don't care about
        if i not in ['img','name']:
            button=buttonDef[i]
            # get code for the key
            keycode=GetKeyCode('KEY',button.get("code","").upper())
            if keycode==None:
                print('Key Code Not Found For : %s'%(button["code"]))
                button["code"]=0
            else:
                button["code"]=keycode

            if button.get("mod",None) != None:
                keycode=GetKeyModCode(button.get("mod","").upper())
                if keycode==None:
                    print('Mod Key Code Not Found For : %s'%(button["mod"]))
                    button["code"]=0
                    button["mod"]=0
                else:
                    button["mod"]=keycode
            else:
                button["mod"]=0

            print('Mapped Button %s - mod %s - code %s'%(i,button["mod"],button["code"]))

            
            


def GetKeyCode(*keynames):
    KeyString="_".join(keynames)
    return KEYCODESLU.get(KeyString,None)

def GetKeyModCode(modKey):
    # parses the potentially mixed names for the mod code
    keys=modKey.split(",")
    finalKeyCode=0
    for key in keys:
        keyCode=GetKeyCode('KEY','MOD',key)
        if keyCode==None:            
            return None
        else:
            finalKeyCode = finalKeyCode | keyCode
    return finalKeyCode
