#region Imports
import chardet # Dependencies: pip install chardet

from lib_io import *
from lib_db import *
#endregion Imports


#region Functions
def getDictOrNone(val) -> dict :
    if type(val) is dict:
        return val
    else:
        return None

#endregion Functions


#region MainCode
def main_test(): # Test

    # asciiStr ='''
    # '''
    # contentBytes = str.encode(asciiStr)
    # result = chardet.detect(contentBytes)
    # logF(result)

    # Try to encode from ASCII to UTF-8
    # utf8 = asciiStr.decode("utf-8") # https://stackoverflow.com/questions/28583565/str-object-has-no-attribute-decode-python-3-error
    

    # contentBytes = str.encode(utf8)
    # result = chardet.detect(contentBytes)
    # logF(result)

    result = getDictOrNone( {} )
    result = getDictOrNone( [] )

    # alter seq
    tableName = "simple_data"
    tableName = "simple_data2"
    colName = "id"
    seqName = f"{tableName}_{colName}_seq"
    result = alterSeq(seqName, 1)

    if not result:
        print("not result")
    else:
        print(result)

    pass


#endregion MainCode


#region Startup
if __name__=="__main__":
    print("Module executed as main")
    main_test()
else:
    print("Module [{0}] imported".format(__name__))
#endregion Startup