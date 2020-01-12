#region Imports
from lib_consts import *
from lib_general_stuff import *
from lib_config import *
from lib_io import *
from lib_chunks_processing import *
from lib_db import *

import log
#endregion Imports

#region MainCode
def main_lib(): # Test
    """"""
    if not logger:
        return

    # global config
    # config = getConfigValues()


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
    
    truncateTable("simple_data")

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
    result = insert(query, params)
    logger.info(result)
#endregion MainCode


#region Startup
logger = log.init()
if __name__=="__main__":
    if logger:
        logger.info(f"This module is executing")
        main_lib()
else:
    logger.info(f"This module is imported")
#endregion Startup