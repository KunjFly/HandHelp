#region Imports
from inspect import stack
from os import path, listdir
import os
import json
from datetime import datetime
from send2trash import send2trash   # !!!!! pip install Send2Trash
import shutil

from lib_consts import *
from lib_general_stuff import *
#endregion Imports


#region MainCode

##############################
#	Logging
##############################

def logMessage(msg, fileName="log", lvl=1, toFile=True, toConsole=True):
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

def writeToFile(obj, fileName=None, filePath=[], mode=None, encoding="utf-8", isAddTS=False):
    funcName = stack()[0][3]

    if mode is None:
        mode="a"

    fileToBeWrite = getPathToOutputFile(fileName, filePath, isAddTS)

    try:
        if type(obj) is dict:
            with open(fileToBeWrite, mode, encoding=encoding) as file:
                json.dump(obj, file, ensure_ascii=False, indent=4)
        else:
            with open(fileToBeWrite, mode, encoding=encoding) as file:
                file.write(obj)

        return True, fileToBeWrite
    except Exception as ex:
        printF("Error in function [{}]. Exception: [{}]", funcName, ex)
        return False, fileToBeWrite


def writeObjsToFilesWitsTSname(objsLst: list, filePath=[], encoding="utf-8"):
    funcName = stack()[0][3]

    for obj in objsLst:
        isSuccess, writedFile = writeToFile(obj, filePath=filePath, isAddTS=True, encoding=encoding)
        if isSuccess:
            logF("{}: File[{}]", funcName, writedFile)
        else:
            warnF("{}: File[{}]", funcName, writedFile)


def writeObjsToFiles(objsLst: list):
    funcName = stack()[0][3]
    
    for obj in objsLst:

        objType = type(obj)
        if objType is not dict:
            warnF("{}: obj has type{}, but it must be dict!", funcName, obj, objType)
            continue
        
        # fields = ("content", "name", "path", "mode" "encoding", "timestamp")
        # if not all( k in obj for k in fields ):
        #     warnF("{}: obj have incorrect strcucture.", funcName)
        #     continue
        
        fileContent = obj["content"] if "content" in obj else None
        fileName = obj["name"] if "name" in obj else None
        filePath = obj["path"] if "path" in obj else None
        fileMode = obj["mode"] if "mode" in obj else None
        fileEncoding = obj["encoding"] if "encoding" in obj else None
        fileTimestamp = obj["timestamp"] if "timestamp" in obj else None
        
        isSuccess, writedFile = writeToFile(fileContent, fileName, filePath, fileMode, fileEncoding, fileTimestamp)
        if isSuccess:
            logF("{}: File[{}]", funcName, writedFile)
        else:
            warnF("{}: File[{}]", funcName, writedFile)


def getPathToInputFile(fileName, filePath=[]):
    if len(filePath) == 0:
        return path.join(ROOT_PATH, fileName)

    filePath.append(fileName)
    return path.join(*filePath)


def getPathToOutputFile(fileName=None, filePath=[], isAddTS=None, ext="txt"):

    if fileName:
        if isAddTS:
            fileName = strF("{}_{}.{}", fileName, getNowTS(), ext)
        else:
            fileName = strF("{}.{}", fileName, ext)
        
    else:
        fileName = strF("{}.{}", getNowTS(), ext)

    if filePath is None or len(filePath) == 0:
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
        errF("{}: Exception: [{}].", funcName, ex)
        return ""


def readFileAsLinesLst(fileName, encoding="utf-8"):
    funcName = stack()[0][3]

    fileToBeRead = getPathToInputFile(fileName, INPUT_FOLDER_LST)
    try:
        with open(fileToBeRead, "r", encoding=encoding) as file:
            return file.readlines()
    except Exception as ex:
        errF("{}: Exception: [{}].", funcName, ex)
        return None


def deleteContentOfFolder(folderPath, isDeleteDirs=False, isSendToTrash=True):
    funcName = stack()[0][3]

    typeOfFolderPath = type(folderPath)
    if typeOfFolderPath is list:
        folderPath = path.join(*folderPath)
    elif typeOfFolderPath is not str:
        warnF("{}: folderPath[{}] incorrect!", funcName, folderPath)
        return

    if not path.isdir(folderPath):
        warnF("{}: Dir[{}] not exists! Nothing to remove", funcName, folderPath)
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
            errF("{}. Exception: [{}].", funcName, ex)


def main_io(): # Test
    # obj = None
    # if obj:
    #     printF(obj)
    # pass
    
    # obj = {
    #     "name":"name"
    #     # ,"path":"path"
    #     ,"encoding":"encoding"
    # }
    # fields = ("name", "path", "encoding")
    # if all( k in obj for k in fields ):
    #     print("eee, boy")

    

    pass

#endregion MainCode


#region Startup
if __name__=="__main__":
    print("Module executed as main")
    main_io()
else:
    print("Module [{0}] imported".format(__name__))
#endregion Startup