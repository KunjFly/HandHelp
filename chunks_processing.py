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
#   I use reg exprs because HTML is invalid in some cases
##############################
def parseChunk(chunk):
	""""""
	if not chunk:
		return None
		
	parsedChunk = {
		"raw_text"          : chunk
		,"is_done"          : False
		,"question_number"  : None
		,"who_asks"         : None
		,"tags"             : None
		,"question"         : None
		,"who_answers"      : None
		,"answer"           : None
		,"answer_date"      : None
		,"raw_text_rest"    : None
		,"problem_place"	: None
	}


	# Get [question_number]
	regExpStr = r"(<a[ ]{0,}name=\".*?\">.*?[№])(.*?)(<\/a>|\/a>)"
	result = re.findall(regExpStr, chunk, flags=re.IGNORECASE)

	if result and len(result) > 0 and len(result[0][1]) > 0:
		fullResult = "".join(result[0])
		result = result[0][1]
		chunk = chunk.replace(fullResult, "") # remove part [question_number] from chunk

		result = result.strip()
		parsedChunk["question_number"] = result
	else:
		parsedChunk["raw_text_rest"] = chunk
		parsedChunk["problem_place"] = "question_number"
		return parsedChunk


	# Get [who_asks]
	regExpStr = r"(<b>|<b><p>|<pb>|<br>)(Вопрос |Спрашивают |Спрашивает |Cпрашивает |Спрашиваете |Пишет |Обращается |Спрашиваешь |Пишут |Дополняет |Пишете |Пишет, |Сапрашивает |Спрашивает|Спраивает |Спрашиваю |Спрашиваеь )(.*?)(<\/b>|!</b>|<br>|\.)"
	result = re.findall(regExpStr, chunk, flags=re.IGNORECASE)

	if result and len(result) > 0 and len(result[0][2]) > 0:
		fullResult = "".join(result[0])
		result = result[0][2]
		chunk = chunk.replace(fullResult, "") # remove part [who_asks] from chunk

		# remove last semicolon if exists
		regExpStr = r"[:]$"
		result = re.sub(regExpStr, "", result)

		result = result.strip()
		parsedChunk["who_asks"] = result
	else:
		parsedChunk["raw_text_rest"] = chunk
		parsedChunk["problem_place"] = "who_asks"
		return parsedChunk


	# Get [tags] (it can be empty)
	# https://stackoverflow.com/questions/11592033/regex-match-text-between-tags
	# <br><i>(<a href="http://www.hand-help.ru/doc2.6.html" class="link2"><b>иное</b></a>)</i>
	regExpStr = r"(<br><i>\()(.*)(\)<\/i>)"
	regExpStr = r"\n\r(<br><i>\()(.*)(\)<\/i>)\n\r"
	
	result = re.findall(regExpStr, chunk, flags=re.IGNORECASE | re.MULTILINE)

	if result and len(result) > 0 and len(result[0][1]) > 0:
		fullResult = "".join(result[0])
		result = result[0][1]
		chunk = chunk.replace(fullResult, "") # remove part [tags] from chunk

		# Remove all HTML tags
		# https://stackoverflow.com/questions/822452/strip-html-from-text-javascript
		regExpStr = r"<[^>]*>?"
		result = re.sub(regExpStr, "", result)

		if result and len(result) > 0:
			result = result.strip()
			# Remove last ")" if exists
			if result[0] == '(':
				result	= result[1:]
			
			# Remove first "(" if exists
			if result[-1] == ')':
				result	= result[:-1]

			result	= result.split(',')
			result	= [x.strip() for x in result]	# trim all vals in list
			parsedChunk["tags"] = result
  

	# Get [who_answers]
	whoAnswers = ""
	# regExpStr = r"(<p><b>|<b><p>|<p>|<b>)( )?(Отвечает|Отаечает|Ответ)([\w\s.-/(/)]*)(:<\/b>|<\/b>|:)"
	regExpStr = r"(<p><b>|<b><p>|<p>|<b>|<p><br>|<P><b><a.*>|<br>)( )?(Отвечает |Отаечает |Ответ |Ответ:|Пишет |Отвеачет |твечает |Отвечаете )(.*?)(:<\/b>|<\/b>|:)"
	
	
	result = re.findall(regExpStr, chunk, flags=re.IGNORECASE)

	if result and len(result) > 0 and len(result[0][3]) is not None:
		whoAnswers = "".join(result[0])
		result = result[0][3]
		
		# remove last semicolon if exists
		regExpStr = r"[:]$"
		result = re.sub(regExpStr, "", result)

		result = result.strip()
		parsedChunk["who_answers"] = result
	else:
		parsedChunk["raw_text_rest"] = chunk
		parsedChunk["problem_place"] = "who_answers"
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

		# TODO: add if result == ''
		

		result = result.strip()
		parsedChunk["question"] = result
	else:
		parsedChunk["raw_text_rest"] = chunk
		parsedChunk["problem_place"] = "question"
		return parsedChunk


	# Get [answer_date]
	# Get last line with date
	regExpStr = r'(<br>)?(\d{1,2}[/.-]\d{2}[/.-]\d{2,4})(\n\r|\.)?(<\/font><\/h2>|<font><\/h2>|<\/font>|<\/h2>|\.)'
	result = re.findall(regExpStr, chunk, flags=re.IGNORECASE | re.MULTILINE)

	if result and len(result) > 0 and len(result[0][1]) > 0:
		parsedChunk["answer_date"] = result[0][1]
	else:
		parsedChunk["raw_text_rest"] = chunk
		parsedChunk["problem_place"] = "answer_date"
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