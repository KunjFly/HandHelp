#region Imports
# import chardet # Dependencies: pip install chardet
import log
import io_extra
import db
import general_stuff
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
    
    # global config
    # config = config.getConfigValues()


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


    # line = "<br>25.06.2017</font></h2>"
    # line = "<br>TEST PETROVICH</h2>"
    # regExpStr = r"((3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2}))"
    # result = re.search(regExpStr, line)
    # if result:
    #     result = result.group()
    
    db.truncateTable("simple_data")

    query = """
        INSERT INTO simple_data (
            raw_text, question_number, who_asks, tags, question, who_answers, answer, answer_date, raw_text_rest
        )
        VALUES (
            %(raw_text)s, %(question_number)s, %(who_asks)s, %(tags)s, %(question)s, %(who_answers)s, %(answer)s, %(answer_date)s, %(raw_text_rest)s
        ) returning id
    """
    params = {
        "raw_text": "raw_text"
		,"question_number": None
		,"who_asks": None
		,"tags": None
		,"question": None
		,"who_answers": None
		,"answer": None
		,"answer_date": None
		,"raw_text_rest": None
    }
    result = db.insert(query, params)
    logger.info(result)
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