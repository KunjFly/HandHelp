#region Startup
if __name__=="__main__":
    print("Module executed as main")
else:
    print("Module [{0}] imported".format(__name__))
#endregion Startup


#region Imports
from inspect import stack
from datetime import datetime
import time
from pathlib import Path
import os
from yaml import safe_load          # !!!!! pip install pyyaml
import re
import shutil
from send2trash import send2trash   # !!!!! pip install Send2Trash
#endregion Imports


#region Constants
ROOT_PATH = Path().absolute()
INPUT_FOLDER_LST = [ROOT_PATH, "files", "input"]
OUTPUT_FOLDER_LST = [ROOT_PATH, "files", "output"]
#endregion Constants


#region Functions

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
        warnF("Warning in function [{}]: input dictionary have type {}", funcName, type(choicesDict))
        return defaultVal
    
    try:
        choicesDict = { str(k):v for k,v in choicesDict.items() }
    except Exception as ex:
        errF("Error in function [{}]. Exception: [{}].", funcName, ex)
        return defaultVal
    
    if type(checkVal) is not str:
        checkVal = str(checkVal)

    return choicesDict.get(checkVal, defaultVal)


def getNowTS(): # Get now timestamp w/ milliseconds
    return time.time() * 1000


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
#	Config
##############################

def loadConfig(fileName="config.yml"):
    funcName = stack()[0][3]
    try:
        filePath = os.path.join(ROOT_PATH, fileName)
        return safe_load( open(filePath) )
    except Exception as ex:
        errF("Error in function [{}]. Exception: [{}].", funcName, ex)


def getConfigValues(config=None):
    funcName = stack()[0][3]

    if not config :
        config = loadConfig()
        if not config :
            warnF("Warning in function [{}]: Config is Empty", funcName)
            return None

    # global DB_URL
    # if hasattr(config, "DB_URL"):
    #     DB_URL = config.DB_URL
    # else:
    #     DB_URL = None

    # SITE_URL
    # FILE_TO_BE_PROCESSED

    return config


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
        return os.path.join(ROOT_PATH, fileName)

    filePath.append(fileName)
    return os.path.join(*filePath)


def getPathToOutputFile(fileName=None, filePath=[]):
    if not fileName or fileName == None:
        fileName = strF("{}.{}", getNowTS(), "txt")

    if len(filePath) == 0:
        return os.path.join(ROOT_PATH, fileName)
    
    outPath = filePath.copy() # To prevent changes to the original list
    outPath.append(fileName)
    return os.path.join(*outPath)


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
        folderPath = os.path.join(*folderPath)
    elif typeOfFolderPath is not str:
        warnF("folderPath[{}] incorrect!", folderPath)
        return

    if not os.path.isdir(folderPath):
        warnF("Dir[{}] not exists! Nothing to remove", folderPath)
        return

    for fileName in os.listdir(folderPath):
        filePath = os.path.join(folderPath, fileName)
        try:
            if os.path.isfile(filePath):

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


##############################
#	Text to Chunks processing
##############################

def linesLstToChunksLst(linesLst):
    # funcName = stack()[0][3]

    chunksLst = []
    chunkText = ""

	# Find tag <hr><h2> in line.
	# Split line with finded separator to find out if line consists part of previous chunk
    regExpStr = r"(.*)(<hr\s*\/?><h2\s*\/?>)(.*)" # Captured 3 groups
    # regExpStr = r"(?:.*)(?:<hr\s*\/?><h2\s*\/?>)(?:.*)" # Non-captured groups
    
    # regExp = re.compile(regExpStr)
    # isMatch = regExp.match(line)

    for line in linesLst:
        
        result = re.findall(regExpStr, line, flags=re.IGNORECASE)

        if result and len(result) > 0:
            
            if len(result[0]) > 0: # Add part of previous chunk if exists
                chunkText += result[0][0]

                # Remove part of previous chunk in line
                line = line.replace(result[0][0], "")
            
            if chunkText and chunkText != "" :
                chunksLst.append(chunkText)
                chunkText = "" # prepare for next chunk

        chunkText += line + "\r"

    # Last chunk in file
    chunksLst.append(chunkText)

    return chunksLst


##############################
#	Processing of chunks
##############################

def parseChunk(chunk):
    # funcName = stack()[0][3]

    if not chunk:
        return
        
    parsedChunk = {
        "raw_text": chunk
		,"question_number": None
		,"who_asks": None
		,"tags": None
		,"question": None
		,"who_answers": None
		,"answer": None
		,"answer_date": None
		,"raw_text_rest": None
    }


    # Get [question_number]
    regExpStr = r"(<a[ ]{0,}name=\".*?\">.*?[№])(.*?)(<\/a>)" # Captured 3 groups
    result = re.findall(regExpStr, chunk, flags=re.IGNORECASE)

    if result and len(result) > 0 and len(result[0][1]) > 0:
        fullResult = "".join(result[0])
        result = result[0][1]
        chunk = chunk.replace(fullResult, "") # remove part [question_number] from chunk

        result = result.strip()
        parsedChunk["question_number"] = result
    else:
        parsedChunk["raw_text_rest"] = chunk
        # TODO: write parsed chunk
        return


    # Get [who_asks]
    regExpStr = r"(<b>Спрашивает[ ]{0,})(.*?)(<\/b>)" # Captured 3 groups
    result = re.findall(regExpStr, chunk, flags=re.IGNORECASE)

    if result and len(result) > 0 and len(result[0][1]) > 0:
        fullResult = "".join(result[0])
        result = result[0][1]
        chunk = chunk.replace(fullResult, "") # remove part [who_asks] from chunk

        # remove last semicolon if exists
        regExpStr = r"[:]$"
        result = re.sub(regExpStr, "", result)

        result = result.strip()
        parsedChunk["who_asks"] = result
    else:
        parsedChunk["raw_text_rest"] = chunk
        # TODO: write parsed chunk
        return


    # Get [tags] (it can be empty)
	# https://stackoverflow.com/questions/11592033/regex-match-text-between-tags
    regExpStr = r"(<i>)(.*?)(<\/i>)" # Captured 3 groups
    result = re.findall(regExpStr, chunk, flags=re.IGNORECASE)

    if result and len(result) > 0 and len(result[0][1]) > 0:
        fullResult = "".join(result[0])
        result = result[0][1]
        chunk = chunk.replace(fullResult, "") # remove part [tags] from chunk

        # Remove all HTML tags
        # https://stackoverflow.com/questions/822452/strip-html-from-text-javascript
        regExpStr = r"<[^>]*>?"
        result = re.sub(regExpStr, "", result)

        # Remove first "(" if exists
        regExpStr = r"^[(]"
        result = result.replace(regExpStr, "")

        # Remove last ")" if exists
        regExpStr = r"[)]$"
        result = result.replace(regExpStr, "")

        result = result.strip()
        parsedChunk["tags"] = result


    # Get [who_answers]
    whoAnswers = ""
    regExpStr = r"(<b>Отвечает[ ]{0,})(.*?)(<\/b>)" # Captured 3 groups
    result = re.findall(regExpStr, chunk, flags=re.IGNORECASE)
    if result and len(result) > 0 and len(result[0][1]) > 0:
        whoAnswers = "".join(result[0])
        result = result[0][1]
        
        # remove last semicolon if exists
        regExpStr = r"[:]$"
        result = re.sub(regExpStr, "", result)

        result = result.strip()
        parsedChunk["who_answers"] = result
    else:
        parsedChunk["raw_text_rest"] = chunk
        # TODO: write parsed chunk
        return

    
    # Get [question]
    result = chunk.split(whoAnswers)
    if result and len(result) > 0:
        result = result[0]
        chunk = chunk.replace(result, "") # remove part [question] from chunk
        chunk = chunk.replace(whoAnswers, "") # remove part [who_answers] from chunk

        # Replace <br> on \r\n
        # https://stackoverflow.com/questions/5959415/jquery-javascript-regex-replace-br-with-n
        regExpStr = r"<br\s*[\/]?>"
        result = re.sub(regExpStr, "\r\n", result)

        # Remove all HTML tags
        regExpStr = r"<[^>]*>?"
        result = re.sub(regExpStr, "", result)

        result = result.strip()
        parsedChunk["question"] = result
    else:
        parsedChunk["raw_text_rest"] = chunk
        # TODO: write parsed chunk
        return


    # Get [answer_date]
	# Get last line with date
    regExpStr = r"^(.*?)(<\/h2>)" # Captured 2 groups
    result = re.findall(regExpStr, chunk, flags=re.IGNORECASE or re.DOTALL) # If error then use "|"
    if result and len(result) > 0 and len(result[0][0]) > 0:
        fullResult = "".join(result[0])
        # Get date
        # https://www.regextester.com/97612
        regExpStr = r"((3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2}))"
        result = re.search(regExpStr, fullResult)
        if result is not None:
            result = result.group()
            parsedChunk["answer_date"] = result

			# Remove part [answer_date] from chunk
            chunk = chunk.replace(fullResult, "")
        else:
            parsedChunk["raw_text_rest"] = chunk
            # TODO: write parsed chunk
            return
    else:
        parsedChunk["raw_text_rest"] = chunk
        # TODO: write parsed chunk
        return
    

    # Get [previous_questions]
    # TODO


    # Get [answer]
	# Replace <br> on \r\n
	# https://stackoverflow.com/questions/5959415/jquery-javascript-regex-replace-br-with-n
    regExpStr = r"<br\s*[\/]?>"
    result = re.sub(regExpStr, "\r\n", result)

    # Remove all HTML tags
    regExpStr = r"<[^>]*>?"
    result = re.sub(regExpStr, "", result)

	result = result.strip()
	chunkObj.answer = result

    parsedChunk["raw_text_rest"] = ""
    
    # TODO: write parsed chunk
    # writeChunk(params);
    pass


#endregion Functions


#region MainCode
def main(): # Test

    # global config
    # config = getConfigValues()

    # dic = {
    #         "a"     : 1
    #         ,"b"    : 2
    # }
    # arr = [1, 2, 3, 9]
    # msg = "{} {} {} {}"

    # print( switch(dic, "c", "Hey") )
    # print( switch(arr, "c") )
    
    # print( len(arr) )
    # print( arr[1:] )

    # strF(msg, 4, 2, 0, 0)
    # strF(msg, 4, 2, 0)

    # log("Hello", "Log!")
    # warn("Hello", "Warn!", "321")
    # err("Hello", "ErR!", "oR")

    # deleteContentOfFolder(OUTPUT_FOLDER_LST)


    # regExpStr = r"(?:<b>Спрашивает[ ]{0,})(?:.*?)(?:<\/b>)" # Non Captured 3 groups
    # result = re.findall(regExpStr, line, flags=re.IGNORECASE)

    # line = "<b>Спрашивает Денис</b>"
    # regExpStr = r"(<b>Спрашивает[ ]{0,})(.*?)(<\/b>)" # Captured 3 groups

    # line = """
    # <br><i>(<a href="http://www.hand-help.ru/doc2.1.7.html" class="link2"><b>сбыт</b></a>,  <a href="http://www.hand-help.ru/doc2.1.8.html" class="link2"><b>приготовление и покушение</b></a>, <a href="http://www.hand-help.ru/doc2.1.43.html" class="link2"><b>обратная сила</b></a>)</i>
    # """
    # regExpStr = r"(<i>)(.*?)(<\/i>)" # Captured 3 groups
    # result = re.findall(regExpStr, line, flags=re.IGNORECASE)
    # resultStr = "".join(result[0])

    line = "<br>25.06.2017</font></h2>"
    line = "<br>OLOLO</h2>"
    regExpStr = r"((3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2}))"
    result = re.search(regExpStr, line)
    if result:
        result = result.group()
    

    pass

main()
#endregion MainCode