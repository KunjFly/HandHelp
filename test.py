#region Imports
# import chardet # Dependencies: pip install chardet
from lib_io import *
from lib_db import *
from lib_general_stuff import *

import log
#endregion Imports


#region Functions
def getDictOrNone(val) -> dict :
    """"""
    if type(val) is dict:
        return val
    else:
        return None

#endregion Functions


#region MainCode
def main_test(): # Test
    """"""
    # asciiStr ='''
    # '''
    # contentBytes = str.encode(asciiStr)
    # result = chardet.detect(contentBytes)
    # logger.info(result)

    # Try to encode from ASCII to UTF-8
    # utf8 = asciiStr.decode("utf-8") # https://stackoverflow.com/questions/28583565/str-object-has-no-attribute-decode-python-3-error
    

    # contentBytes = str.encode(utf8)
    # result = chardet.detect(contentBytes)
    # logger.info(result)


    # result = getDictOrNone( {} )
    # result = getDictOrNone( [] )


    # alter seq
    # tableName = "simple_data"
    # tableName = "simple_data2"
    # colName = "id"
    # seqName = f"{tableName}_{colName}_seq"
    # result = alterSeq(seqName, 1)

    # if not result:
    #     logger.info("not result")
    # else:
    #     logger.info(result)
    
    # logger.debug('debug')
    # logger.info('info')
    # logger.warning('warning')
    # logger.error('error')
    # logger.critical('critical')
    
    result  = None
    if not result:
        logger.error("NOT OK")
    else:
        logger.info("OK")
#endregion MainCode


#region Startup
logger = log.init()
if __name__=="__main__":
    if logger:
        logger.info(f"This module is executing")
        main_test()
else:
    logger.info(f"This module is imported")
#endregion Startup