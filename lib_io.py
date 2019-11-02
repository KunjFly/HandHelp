#region Imports
from inspect import stack
from os import path, listdir
import os

from datetime import datetime
from send2trash import send2trash   # !!!!! pip install Send2Trash
import shutil

from lib_consts import *
from lib_general_stuff import *
# from lib_logging import *
#endregion Imports


#region MainCode

##############################
#	Logging
##############################

def logMessage(msg, fileName="log.txt", lvl=1, toFile=True, toConsole=True):
    # Prepare message
    msg = str(msg)

    now = datetime.now()
    nowFormatted = "{}-{}-{} {}:{}:{}:{}"
    nowFormatted = nowFormatted.format(now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond)

    lvls = {0:"DEBUG", 1:"INFO", 2:"WARN", 3:"ERROR"}
    lvlName = switch(lvls, lvl, "INFO")

    msg = f"[{nowFormatted}]\t[{lvlName}]\t{msg}\r"

    if toFile:
        writeToFile(msg, fileName=fileName)

    if toConsole:
        print(msg)


def log(*msgs):
    funcName = stack()[0][3]

    try:
        msg = " ".join(msgs)
        logMessage(msg)
    except Exception as ex:
        printF("Error in function [{}]. Exception: [{}].", funcName, ex)


def warn(*msgs):
    funcName = stack()[0][3]

    try:
        msg = " ".join(msgs)
        logMessage(msg, lvl=2)
    except Exception as ex:
        printF("Error in function [{}]. Exception: [{}].", funcName, ex)


def err(*msgs):
    funcName = stack()[0][3]
    
    try:
        msg = " ".join(msgs)
        logMessage(msg, lvl=3)
    except Exception as ex:
        printF("Error in function [{}]. Exception: [{}].", funcName, ex)


def logF(*args):
    funcName = stack()[0][3]
    
    try: 
        log( strF(*args) )
    except Exception as ex:
        printF("Error in function [{}]. Exception: [{}].", funcName, ex)


def warnF(*args):
    funcName = stack()[0][3]
    
    try:
        warn( strF(*args) )
    except Exception as ex:
        printF("Error in function [{}]. Exception: [{}].", funcName, ex)


def errF(*args):
    funcName = stack()[0][3]
    
    try:
        msg = strF(*args)
        err(msg)
    except Exception as ex:
        printF("Error in function [{}]. Exception: [{}].", funcName, ex)


##############################
#	I/O
##############################

def writeToFile(text, fileName=None, filePath=[], mode="a"):
    funcName = stack()[0][3]

    fileToBeWrite = getPathToOutputFile(fileName, filePath)

    try:
        with open(fileToBeWrite, mode) as file:
            file.write(text)
        return True, fileToBeWrite
    except Exception as ex:
        printF("Error in function [{}]. Exception: [{}]", funcName, ex)
        return False, fileToBeWrite


def writeToFiles(textsLst, fileNames=[], filePath=[]):
    for text in textsLst:
        isSuccess, writedFile = writeToFile(text, filePath=filePath)

        if isSuccess:
            logF("writeToFiles: Success[{}], File[{}]", isSuccess, writedFile)
        else:
            errF("writeToFiles: Success[{}], File[{}]", isSuccess, writedFile)



def getPathToInputFile(fileName, filePath=[]):
    if len(filePath) == 0:
        return path.join(ROOT_PATH, fileName)

    filePath.append(fileName)
    return path.join(*filePath)


def getPathToOutputFile(fileName=None, filePath=[]):
    if not fileName or fileName == None:
        fileName = strF("{}.{}", getNowTS(), "txt")

    if len(filePath) == 0:
        return path.join(ROOT_PATH, fileName)
    
    outPath = filePath.copy() # To prevent changes to the original list
    outPath.append(fileName)
    return path.join(*outPath)


def readFileAsStr(fileName):
    funcName = stack()[0][3]

    fileToBeRead = getPathToInputFile(fileName, INPUT_FOLDER_LST)
    try:
        with open(fileToBeRead, "r") as file:
            return file.read()
    except Exception as ex:
        errF("Error in function [{}]. Exception: [{}].", funcName, ex)
        return ""


def readFileAsLinesLst(fileName):
    funcName = stack()[0][3]

    fileToBeRead = getPathToInputFile(fileName, INPUT_FOLDER_LST)
    try:
        with open(fileToBeRead, "r") as file:
            return file.readlines()
    except Exception as ex:
        errF("Error in function [{}]. Exception: [{}].", funcName, ex)
        return None


def deleteContentOfFolder(folderPath, isDeleteDirs=False, isSendToTrash=True):
    funcName = stack()[0][3]

    typeOfFolderPath = type(folderPath)
    if typeOfFolderPath is list:
        folderPath = path.join(*folderPath)
    elif typeOfFolderPath is not str:
        warnF("folderPath[{}] incorrect!", folderPath)
        return

    if not path.isdir(folderPath):
        warnF("Dir[{}] not exists! Nothing to remove", folderPath)
        return

    for fileName in listdir(folderPath):
        filePath = path.join(folderPath, fileName)
        try:
            if path.isfile(filePath):

                if isSendToTrash:
                    send2trash(filePath)
                    logF("Success move to trash file [{}]", filePath)
                else:
                    os.unlink(filePath)
                    logF("Success delete file [{}]", filePath)
                
            elif isDeleteDirs and os.path.isdir(filePath):

                if isSendToTrash:
                    send2trash(filePath)
                    logF("Success move to trash dir [{}]", filePath)
                else:
                    shutil.rmtree(filePath)
                    logF("Success delete dir [{}]", filePath)

        except Exception as ex:
            errF("Error in function [{}]. Exception: [{}].", funcName, ex)
#endregion MainCode


#region Startup
if __name__=="__main__":
    print("Module executed as main")
else:
    print("Module [{0}] imported".format(__name__))
#endregion Startup