#region Imports
from inspect import stack
import time
#endregion Imports


#region MainCode
##############################
#	General stuff
##############################

def strF(*args): # Format string, 0 - str, 1..N - args for .format(...)
    funcName = stack()[0][3]
    argsLen = len(args)

    if argsLen == 0 or argsLen is None :
        return ""
    elif argsLen == 1 :
        return str(args[0])
    else:
        msg = str(args[0])
        argsLst = args[1:]

        try:
            msg = msg.format(*argsLst)
        except Exception as ex:
            msg = "Error in function [{}]. Exception: [{}]. Message: [{}]"
            msg = msg.format(funcName, ex, args[0])
        finally:
            return msg


def printF(*args):
    print( strF(*args) )
        

def switch(choicesDict, checkVal, defaultVal=False): # Coz there is no [switch] in Py
    funcName = stack()[0][3]

    if type(choicesDict) is not dict:
        # warnF
        print("Warning in function [{}]: input dictionary have type {}", funcName, type(choicesDict))
        return defaultVal
    
    try:
        choicesDict = { str(k):v for k,v in choicesDict.items() }
    except Exception as ex:
        # errF
        print("Error in function [{}]. Exception: [{}].", funcName, ex)
        return defaultVal
    
    if type(checkVal) is not str:
        checkVal = str(checkVal)

    return choicesDict.get(checkVal, defaultVal)


def getNowTS(): # Get now timestamp w/ milliseconds
    return time.time() * 1000
#endregion MainCode


#region Startup
if __name__=="__main__":
    print("Module executed as main")
else:
    print("Module [{0}] imported".format(__name__))
#endregion Startup