# region Imports
from inspect import stack

import lib
from lib_io import *
# endregion Imports


# region MainCode
def main():
    funcName = stack()[0][3]

    lib.log("[Start script]")

    lib.deleteContentOfFolder(lib.OUTPUT_FOLDER_LST)

    # fileName = "test-10-chunks.html"
    fileName = "test-100-chunks.html"
    # fileName = "test-1000-chunks.html"
    # fileName = "doc1-11499.html"

    # read file
    # linesLst = lib.readFileAsLinesLst(fileName, encoding="ascii")
    # linesLst = lib.readFileAsLinesLst(fileName, encoding="latin-1")
    linesLst = lib.readFileAsLinesLst(fileName, encoding="Windows-1251")

    # get chunks
    chunksLst = lib.linesLstToChunksLst(linesLst)
    if not chunksLst:
        warnF("{}: chunksLst is Empty!", funcName)
        return

    # parse chunks
    parsedChunksLst = []
    for chunk in chunksLst:
        parsedChunk = lib.parseChunk(chunk)
        if parsedChunk:
            parsedChunksLst.append(parsedChunk)
    

    # write chunks to file
    # lib.writeObjsToFilesWitsTSname(chunksLst, filePath=lib.OUTPUT_FOLDER_LST)

    # write chunks to file [splited on successed and failed]
    successParsedChunks = list()
    problemParsedChunks = list()
    for parsedChunk in parsedChunksLst:
        if not parsedChunk["raw_text_rest"]:
            del parsedChunk["raw_text_rest"]
            itemToBeWrited = {
                "content" : parsedChunk
                ,"name" : "Success"
                ,"path" : lib.OUTPUT_FOLDER_LST
                # ,"encoding" : "cp-1251"
                # ,"encoding" : "cyrillic"
                # ,"encoding" : "cp1251"
                ,"timestamp": True
            }
            successParsedChunks.append(itemToBeWrited)
        else:
            itemToBeWrited = {
                "content" : parsedChunk
                ,"name" : "Fiasko"
                ,"path" : lib.OUTPUT_FOLDER_LST
                # ,"encoding" : "cp-1251"
                # ,"encoding" : "cyrillic"
                # ,"encoding" : "cp1251"
                ,"timestamp": True
            }
            problemParsedChunks.append(itemToBeWrited)
        
    
    # write success parsed chunks to file
    lib.writeObjsToFiles(successParsedChunks)
    lib.writeObjsToFiles(problemParsedChunks)


    # TODO: write parsed chunk to DB

    lib.log("[End script]")
# endregion MainCode


# region Startup
if __name__ == "__main__":
    print("Module executed as main")
    main()
else:
    print("Module [{0}] imported".format(__name__))
# endregion Startup