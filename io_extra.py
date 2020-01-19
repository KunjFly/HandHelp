#region Imports
from inspect import stack
from os import path, listdir
import os
import json
from datetime import datetime
from send2trash import send2trash # Dependencies: pip install Send2Trash
import shutil

import log
import consts
import general_stuff
#endregion Imports


#region Functions
##############################
#	I/O
##############################
def writeToFile(obj, fileName=None, filePath=[], mode=None, encoding="utf-8", isAddTS=False):
    """"""
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
        logger.error("Exception occurred!", exc_info=True)
        return False, fileToBeWrite


def writeObjsToFilesWithTSname(objsLst: list, filePath=[], encoding="utf-8"):
    """"""
    for obj in objsLst:
        isSuccess, writedFile = writeToFile(obj, filePath=filePath, isAddTS=True, encoding=encoding)
        if isSuccess:
            logger.info(f"File[{writedFile}]")


def writeObjsToFiles(objsLst: list):
    """"""
    for obj in objsLst:

        objType = type(obj)
        if objType is not dict:
            logger.warning(f"Obj has type [{objType}], but it must be dict!")
            continue
        
        # fields = ("content", "name", "path", "mode" "encoding", "timestamp")
        # if not all( k in obj for k in fields ):
        #     logger.warning("Obj have incorrect strcucture.")
        #     continue
        
        fileContent = obj["content"] if "content" in obj else None
        fileName = obj["name"] if "name" in obj else None
        filePath = obj["path"] if "path" in obj else None
        fileMode = obj["mode"] if "mode" in obj else None
        fileEncoding = obj["encoding"] if "encoding" in obj else None
        fileTimestamp = obj["timestamp"] if "timestamp" in obj else None
        
        isSuccess, writedFile = writeToFile(fileContent, fileName, filePath, fileMode, fileEncoding, fileTimestamp)
        if isSuccess:
            logger.info(f"File[{writedFile}]")


def getPathToInputFile(fileName, filePath=[]):
    """"""
    if len(filePath) == 0:
        return path.join(consts.ROOT_PATH, fileName)

    filePath.append(fileName)
    return path.join(*filePath)


def getPathToOutputFile(fileName=None, filePath=[], isAddTS=None, ext="txt"):
    """"""
    nowTS       = general_stuff.getNowTS()
    if fileName:
        if isAddTS:
            fileName    = f"{fileName}_{nowTS}.{ext}"
        else:
            fileName    = f"{fileName}.{ext}"
    else:
        fileName    = f"{nowTS}.{ext}"

    if filePath is None or len(filePath) == 0:
        return path.join(consts.ROOT_PATH, fileName)
    
    outPath = filePath.copy() # To prevent changes to the original list
    outPath.append(fileName)
    return path.join(*outPath)


def readFileAsStr(fileName):
    """"""
    fileToBeRead = getPathToInputFile(fileName, consts.INPUT_FOLDER_LST)
    try:
        with open(fileToBeRead, "r") as file:
            return file.read()
    except Exception as ex:
        logger.error("Exception occurred!", exc_info=True)
        return ""


def readFileAsLinesLst(fileName, encoding="utf-8", errors="replace"):
    """"""
    fileToBeRead = getPathToInputFile(fileName, consts.INPUT_FOLDER_LST)
    try:
        with open(fileToBeRead, "r", encoding=encoding, errors=errors) as file:
            return file.readlines()
    except Exception as ex:
        logger.error("Exception occurred!", exc_info=True)
        return None


def deleteContentOfFolder(folderPath, isDeleteDirs=False, isSendToTrash=True):
    """"""
    typeOfFolderPath = type(folderPath)
    if typeOfFolderPath is list:
        folderPath = path.join(*folderPath)
    elif typeOfFolderPath is not str:
        logger.warning(f"FolderPath[{folderPath}] is incorrect!")
        return

    if not path.isdir(folderPath):
        logger.warning(f"Dir[{folderPath}] not exists! Nothing to remove")
        return

    for fileName in listdir(folderPath):
        filePath = path.join(folderPath, fileName)
        try:
            if path.isfile(filePath):

                if isSendToTrash:
                    send2trash(filePath)
                    logger.info(f"Success move to trash file [{filePath}]")
                else:
                    os.unlink(filePath)
                    logger.info(f"Success delete file [{filePath}]")
                
            elif isDeleteDirs and os.path.isdir(filePath):

                if isSendToTrash:
                    send2trash(filePath)
                    logger.info(f"Success move to trash dir [{filePath}]")
                else:
                    shutil.rmtree(filePath)
                    logger.info(f"Success delete dir [{filePath}]")

        except Exception as ex:
            logger.error("Exception occurred!", exc_info=True)
#endregion Functions


#region Startup
logger = log.init()
if __name__=="__main__":
    if logger:
        logger.info(f"This module is executing")
else:
    logger.info(f"This module is imported")
#endregion Startup