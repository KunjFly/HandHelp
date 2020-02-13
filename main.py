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
    logger.info("==================================================")
    logger.info("[Start script]")


    """ 
    clear output and read input
     """
    io_extra.deleteContentOfFolder(consts.OUTPUT_FOLDER_LST)
    fileName = "test-1-chunk.html"
    # fileName = "test-10-chunks.html"
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
    for chunk in parsedChunksLst:
        
        # [raw_consultations]
        txt         = chunk["raw_text"]
        txt_rest    = chunk["raw_text_rest"]
        is_done     = 1 if chunk["is_done"] is True else 0
        query       = f"""
            Insert into raw_consultations (txt, txt_rest, is_done)
            values ('{txt}', '{txt_rest}', {is_done})
            returning id
        """
        result      = postgres_db.qExec(query)
        if not result:
            continue
        id_raw      = result
        logger.info(f"id_raw returning id = {id_raw}")
                
        
        # [consultations]
        c_number    = chunk["question_number"]
        c_date      = chunk["answer_date"]
        c_date      = f"to_timestamp('{c_date}', 'dd.mm.yyyy')"
        query       = f"""
            Insert into consultations (c_number, id_raw, c_date)
            values ({c_number}, {id_raw}, {c_date})
            returning id
        """
        result      = postgres_db.qExec(query)
        if not result:
            continue
        
        id_consultation = result
        logger.info(f"id_consultation returning id = {id_raw}")
        

        # [tags], [consultation_tags]
        # TODO: remove brackets and parse tags by "comma"
        txt         = chunk["tags"]
        query       = f"""
            select id from tags
            where txt = '{txt}'
        """
        result      = postgres_db.qExec(query)
        if result is False:
            continue
        
        # Check if tag not exists in table
        if len(result):
            id_tag      = result[0][0]
            logger.info(f"id_tag exists = {id_tag}")
        else:
            query       = f"""
                Insert into tags (txt)
                values ('{txt}')
                returning id
            """
            result      = postgres_db.qExec(query)
            if not result:
                continue
            
            id_tag      = result
            logger.info(f"id_tag returning id = {id_tag}")
        
        query       = f"""
            Insert into consultation_tags (id_consultation, id_tag)
            values ('{id_consultation}', '{id_tag}')
        """
        result      = postgres_db.qExec(query)
        if not result:
            continue
        
        
        # [answers], [consultants], [consultant_answers]
        txt    = chunk["answer"]
        query       = f"""
            Insert into answers (txt)
            values ('{txt}')
            returning id
        """
        result      = postgres_db.qExec(query)
        if not result:
            continue
        
        id_answer   = result
        logger.info(f"id_answer returning id = {id_answer}")
        
        
        name    = chunk["who_answers"]
        query       = f"""
            Insert into consultants (name)
            values ('{name}')
            returning id
        """
        result      = postgres_db.qExec(query)
        if not result:
            continue
        
        id_consultant   = result
        logger.info(f"id_consultant returning id = {id_consultant}")
        
        
        query       = f"""
            Insert into consultant_answers (id_consultation, id_consultant, id_answer)
            values ({id_consultation}, {id_consultant}, {id_answer})
        """
        result      = postgres_db.qExec(query)
        if not result:
            continue
        
        
        # [questions], [asking_persons]
        txt    = chunk["question"]
        query       = f"""
            Insert into questions (id_consultation, txt)
            values ({id_consultation}, '{txt}')
        """
        result      = postgres_db.qExec(query)
        if not result:
            continue
        
        
        name    = chunk["who_asks"]
        query       = f"""
            Insert into asking_persons (id_consultation, name)
            values ({id_consultation}, '{name}')
        """
        result      = postgres_db.qExec(query)
        if not result:
            continue
        
        
        # TODO: fill [categories], [consultation_categories]
        pass

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