#region Imports
from inspect import stack
import re

import log
import io_extra
#endregion Imports


#region Functions
##############################
#	Text to Chunks processing
##############################
def linesLstToChunksLst(linesLst):
    """"""
    if not linesLst:
        logger.warning("Input parameter [linesLst] is empty!")
        return

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
    """"""
    if not chunk:
        return None
        
    parsedChunk = {
        "raw_text"          : chunk     # +
        ,"is_done"          : False     # +
		,"question_number"  : None      # +
		,"who_asks"         : None      # +
		,"tags"             : None      # +
		,"question"         : None      # +
		,"who_answers"      : None      # +
		,"answer"           : None      # +
		,"answer_date"      : None      # +
		,"raw_text_rest"    : None      # +
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
        return parsedChunk


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
        return parsedChunk


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
        return parsedChunk

    
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
        return parsedChunk


    # Get [answer_date]
	# Get last line with date
    regExpStr = r"^(.*?)(<\/h2>)" # Captured 2 groups
    # result = re.findall(regExpStr, chunk, flags=re.IGNORECASE or re.DOTALL) # If error then use "|"
    result = re.findall(regExpStr, chunk, flags=re.IGNORECASE | re.DOTALL)
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
            chunk = chunk.replace(result, "")
        else:
            parsedChunk["raw_text_rest"] = chunk
            return parsedChunk
    else:
        parsedChunk["raw_text_rest"] = chunk
        return parsedChunk
    

    # Get [previous_questions]
    # TODO


    # Get [answer]
	# Replace <br> on \r\n
	# https://stackoverflow.com/questions/5959415/jquery-javascript-regex-replace-br-with-n
    regExpStr = r"<br\s*[\/]?>"
    result = re.sub(regExpStr, "\r\n", chunk)

    # Remove all HTML tags
    regExpStr = r"<[^>]*>?"
    result = re.sub(regExpStr, "", result)

    result = result.strip()
    parsedChunk["answer"] = result


    parsedChunk["is_done"] = True    
    return parsedChunk
#endregion Functions


#region Startup
logger = log.init()
if __name__=="__main__":
    if logger:
        logger.info(f"This module is executing")
else:
    logger.info(f"This module is imported")
#endregion Startup