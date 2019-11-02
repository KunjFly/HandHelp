#region Imports
from lib_consts import *
from lib_general_stuff import *
from lib_config import *
from lib_io import *
from lib_chunks_processing import *
#endregion Imports


#region Functions
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
    
#endregion MainCode


#region Startup
if __name__=="__main__":
    print("Module executed as main")
    main()
else:
    print("Module [{0}] imported".format(__name__))
#endregion Startup