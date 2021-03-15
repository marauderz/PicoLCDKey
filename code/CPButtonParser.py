from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode

def parseButtons(buttonDef):
    for i in buttonDef:
        # ignore things we don't care about
        if i not in ['img','name','color']:
            button=buttonDef[i]
            keycodes=[]

            #Support for consumer control button
            #Note to self, might regret putting 
            # the CC indicator flag like this in 
            # the button
            isCCKey=False
            if button.get("type",None)=="cc":
                isCCKey=True
                button["isCC"]=True
            else:
                button["isCC"]=False

            #print('Reading Key : %s'%(i))
            #Create the keycode array from the keys array
            for key in button["keys"]:
                if isCCKey==True:
                    #Consumer Control Button    
                    readCode=getattr(ConsumerControlCode,key.upper(),None)
                    if readCode==None:
                        raise ValueError("Failed to parse key: %s  keycode: %s"%(i, key))
                        break
                    else:
                        keycodes.append(readCode)
                else:
                    readCode=getattr(Keycode,key.upper(),None)
                    if readCode==None:
                        raise ValueError("Failed to parse key: %s  keycode: %s"%(i, key))
                        break
                    else:
                        keycodes.append(readCode)
            button['keycodes']=keycodes
            

