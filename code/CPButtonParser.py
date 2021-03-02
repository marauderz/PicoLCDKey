from adafruit_hid.keycode import Keycode

def parseButtons(buttonDef):
    for i in buttonDef:
        # ignore things we don't care about
        if i not in ['img','name','color']:
            button=buttonDef[i]
            keycodes=[]
            #print('Reading Key : %s'%(i))
            #Create the keycode array from the keys array
            for key in button["keys"]:
                readCode=getattr(Keycode,key.upper(),None)
                if readCode==None:
                    raise ValueError("Failed to parse key: %s  keycode: %s"%(i, key))
                    keycodes=None
                    break
                else:
                    keycodes.append(readCode)
            button['keycodes']=keycodes
            

