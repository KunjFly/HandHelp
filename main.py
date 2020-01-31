# region Imports
from inspect import stack

import log
import consts
import io_extra
import chunks_processing
import postgres_db
# endregion Imports


# region MainCode
def main():
    """"""
    logger.info("[Start script]")


    """ 
    clear output and read input
     """
    io_extra.deleteContentOfFolder(consts.OUTPUT_FOLDER_LST)
    fileName = "test-10-chunks.html"
    # fileName = "test-100-chunks.html"
    # fileName = "test-1000-chunks.html"
    # fileName = "doc_1-11499.html"
    # fileName = "doc_11500-13157.html"

    # linesLst = lib.readFileAsLinesLst(fileName, encoding="ascii")
    # linesLst = lib.readFileAsLinesLst(fileName, encoding="latin-1")
    linesLst = io_extra.readFileAsLinesLst(fileName, encoding="Windows-1251")
    
    
    """ 
    Get chunks
     """
    chunksLst = chunks_processing.linesLstToChunksLst(linesLst)
    if not chunksLst:
        logger.warning("chunksLst is empty!")
        return
    
    logger.info(f"File {fileName} is loaded.")
    
    
    """ 
    Parse chunks
     """
    parsedChunksLst = []
    for chunk in chunksLst:
        parsedChunk = chunks_processing.parseChunk(chunk)
        if parsedChunk:
            parsedChunksLst.append(parsedChunk)
    
    """ 
    Write chunks to files
     """
    # io_extra.writeObjsToFilesWithTSname(chunksLst, filePath=consts.OUTPUT_FOLDER_LST)
    successParsedChunks = list()
    problemParsedChunks = list()
    for parsedChunk in parsedChunksLst:
        if not parsedChunk["raw_text_rest"]:
            # del parsedChunk["raw_text_rest"]
            name           = "SUCCESS_" + parsedChunk["question_number"]
            
            itemToBeWrited = {
                "content"       : parsedChunk
                ,"name"         : name
                ,"path"         : consts.OUTPUT_FOLDER_LST
                ,"timestamp"    : False
            }
            successParsedChunks.append(itemToBeWrited)
        else:
            name    = "FAIL"
            isTS    = True
            
            if parsedChunk["question_number"]:
                name        = "FAIL_" + parsedChunk["question_number"]
                isTS        = False
            
            itemToBeWrited = {
                "content"       : parsedChunk
                ,"name"         : name
                ,"path"         : consts.OUTPUT_FOLDER_LST
                ,"timestamp"    : isTS
            }
            problemParsedChunks.append(itemToBeWrited)

    io_extra.writeObjsToFiles(successParsedChunks)
    io_extra.writeObjsToFiles(problemParsedChunks)

    
    """ 
    Write chunks to DB
     """

    ### Successed
    for chunk in successParsedChunks:
        
        # insert into [raw_consultations]
        raw_text    = chunk.raw_text
        is_done     = chunk.is_done
        query       = f"""
            Insert into raw_consultations (txt, is_done)
            values ({raw_text}, {is_done})
        """
        result      = postgres_db.qExec(query)
        if not result:
            continue
        
        # insert into [consultations]
        question_number    = chunk.question_number
        is_done            = chunk.is_done
        query              = f"""
            Insert into raw_consultations (txt, is_done)
            values ({raw_text}, {is_done})
        """
        result      = postgres_db.qExec(query)
        if not result:
            continue

        # tags

        # consultation_tags

        # answers
        
        # consultants
        
        # consultant_answers
        
        # categories
        
        # consultation_categories
        
        # questions
        
        # asking_persons
        
        
    ### Fiasked
    for chunk in successParsedChunks:

        # raw_consultations


    logger.info("[End script]")
# endregion MainCode


#region Startup
logger = log.init()
if __name__=="__main__":
    if logger:
        logger.info(f"This module is executing")
        main()
else:
    logger.info(f"This module is imported")
#endregion Startup