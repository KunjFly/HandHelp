#region Imports
from inspect import stack
import re
import os
import html

import log
import io_extra
import general_stuff
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

		chunkText += line

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
		,"note"				: None
	}


	# Replace HTML entities
	chunk	= html.unescape(chunk)


	# Get [question_number]
	regExpStr	= r"(<a[ ]{0,}name=\".*?\">.*?[№])(.*?)(<\/a>|\/a>)"
	result		= re.findall(regExpStr, chunk, flags=re.IGNORECASE)

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
	

	# Get [note]  (it can be empty)
	regExpStr	= r"(<br><font .*color=\"red\">|<br><font .*color=\"red\"><b>|<br><b><font .*color=\"Red\">ВНИМАНИЕ!<\/font><\/b>\n|<b><font .*color=\"Red\">ВНИМАНИЕ!<\/font><\/b>\n)(.*)(\n.*)?(<\/b><\/a><\/font>\.|<\/b><\/a><\/font>|<\/b><\/b><\/a><br>\.|<\/b><\/b><\/a><br>|<\/b><\/font><\/h2>|<\/b><\/font><\/font><\/h2>)"
	result		= re.findall(regExpStr, chunk, flags=re.IGNORECASE | re.MULTILINE)

	if result and len(result) > 0:

		notesfullResult	= ""
		for item in result:
			note	= "".join(item)
			chunk		= chunk.replace(note, "") # remove part [note] from chunk

			if notesfullResult == "":
				notesfullResult	= note
			else:
				notesfullResult	+= ";\n" + note
		
		notesfullResult = notesfullResult.strip()
		parsedChunk["note"] = notesfullResult
	

	# Get previous consultations (TODO)
	"""
Examples:

<br>предыдущий <a href="http://hand-help.ru/doc2.7.html#vopr11481" class="link2"><b>11481</b></a>

<br><a href="http://www.hand-help.ru/doc2.1.13.html" class="link2"><b>Предыдущий</b></a> № 10899

<br>предыдущий<a href="http://www.hand-help.ru/doc2.1.17.html" class="link2"><b>11076</b></a> 

<br>предыдущий вопрос<a href="http://www.hand-help.ru/doc2.1.17.html" class="link2"><b>№11081</b></a>

<br>предыдущий 11122

<br>Предыдущий №10934

<br><a href="http://www.hand-help.ru/doc2.1.7.html" class="link2"><b>Предыдущий вопрос №10979</b></a>.

<br>предыдущий вопрос № 11005

<br>предыдущий 11008, 11006

<br>Предыдущий 10980 <a href="http://hand-help.ru/doc2.12.html" class="link2"><b>в международной защите</b></a>

<br>предыдущий № 10901

<br>предыдущий вопрос <b>№ 10891</b>

<br>предыдущий вопрос<a href="http://www.hand-help.ru/doc2.1.1.html#vopr10858" class="link2"><b>№10858</b></a> 

<br>Предыдущие вопросы №№:<a href="http://www.hand-help.ru/doc2.9.html#10620" class="link2"><b>№10620</b></a>, <a href="http://www.hand-help.ru/doc2.9.html#10649" class="link2"><b>№10649</b></a>, <a href="http://www.hand-help.ru/doc2.1.51.html#10657" class="link2"><b>№10657</b></a>.

<br>предыдущий <a href="http://www.hand-help.ru/doc2.1.13.html#vopr10434" class="link2"><b>№ 10434</b></a>

<br><b>(предыдущий: №10196)</b>

<br><b>(предыдущий 10167 в рубрике «<a href="http://hand-help.ru/doc2.1.3.html" class="link2"><b>размеры</b></a>»)</b>

<br><i>(предыдущий 10046 <a href="http://www.hand-help.ru/doc2.1.7.html" class="link2"><b>сбыт</b></a>)</i>

<br><b><i>(Предыдущий:№9946)</i></b>

<br><i>(предыдущий 9989)</i>

<br>Предыдущий <a href="http://hand-help.ru/doc2.1.13.html#vopr664" class="link2"><b>вопрос № 664</b></a>.

<br>Предыдущий <a href="http://hand-help.ru/doc15.html#vopr10852" class="link2"><b>10852</b></a> и <a href="http://hand-help.ru/doc2.1.13.html#vopr12875" class="link2"><b>12875</b></a>

<br>предыдущий <a href="http://hand-help.ru/doc2.12.html#vopr7333" class="link2"><b>№ 7333</b></a>

<br><i>предыдущий <a href="http://hand-help.ru/doc2.1.13.html#vopr7348" class="link2"><b>№ 7348</b></a></i>

	"""


	# Get [who_asks]
	regExpStr	= r"(<b>|<b><p>|<pb>|<br>)(Вопрос |Спрашивают |Спрашивает |Cпрашивает |Спрашиваете |Пишет |Обращается |Спрашиваешь |Пишут |Дополняет |Пишете |Пишет, |Сапрашивает |Спрашивает|Спраивает |Спрашиваю |Спрашиваеь |Спрашиват | Спрашивает |Спращивает |Скрашивает |Спрашиваеьт |Српрашивает |Спрашвиает |Спрашиванет |CСпрашивает |Спрашивае |Спрашивет |Спрашишвает |Спрашвает |Cпрашиваетт |Спрашивали |Спрашшивает )(.*?)(<\/b>|!<\/b>|<br>|\.:<\/b>|\.<\/b>|\.:|\.)"
	result		= re.findall(regExpStr, chunk, flags=re.IGNORECASE)

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
	regExpStr	= r"\n(<br><i>\()(.*)(\)<\/i>)\n"
	result		= re.findall(regExpStr, chunk, flags=re.IGNORECASE | re.MULTILINE)

	if result and len(result) > 0 and len(result[0][1]) > 0:
		fullResult = "".join(result[0])
		result = result[0][1]
		chunk = chunk.replace(fullResult, "") # remove part [tags] from chunk

		# result	= general_stuff.removeHtmlTags(result)

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
	whoAnswers	= ""
	regExpStr	= r"(<p><b>|<b><p>|<p>|<b>|<p><br>|<P><b><a.*>|<br>|<br><\/b>|<br><b>|<<br>b>|<br><b\.|<br><br>БиЮ|<br><br><b>)( )?(Отвечает |Отаечает |Ответ |Ответ:|Пишет |Отвеачет |твечает |Отвечаете |Отвечает |Отвеачает |Отвевает |Отвечает<a.*><b> |Отвечают )(.*?)(:<\/b>|<\/b>|:)"
	result		= re.findall(regExpStr, chunk, flags=re.IGNORECASE)

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

		# Replace <br> on new line
		# https://stackoverflow.com/questions/5959415/jquery-javascript-regex-replace-br-with-n
		# regExpStr = r"<br\s*[\/]?>"
		# result = re.sub(regExpStr, os.linesep, result)

		# result	= general_stuff.removeHtmlTags(result)

		result = result.strip()
		parsedChunk["question"] = result
	else:
		parsedChunk["raw_text_rest"] = chunk
		parsedChunk["problem_place"] = "question"
		return parsedChunk


	# Get [answer_date]
	# Get last line with date
	answerDate	= ""
	regExpStr	= r"(<br>|<br>\n|\n</ol>|</ol>\n|</ul>\n|\n)(\d{1,2}[/.-]\d{2}[/.-]\d{2,4})(\n|\.)?(<\/font><\/h2>|<font><\/h2>|<\/font>|<\/h2>|\.|</b></font>)"
	result		= re.findall(regExpStr, chunk, flags=re.IGNORECASE | re.MULTILINE)

	if result and len(result) > 0 and len(result[-1][1]) > 0:
		parsedChunk["answer_date"]	= result[-1][1]
		answerDate					= "".join(result[-1])
		chunk						= chunk.replace(answerDate, "") # remove part [answer_date] from chunk
	else:
		parsedChunk["raw_text_rest"] = chunk
		parsedChunk["problem_place"] = "answer_date"
		return parsedChunk


	# Get [answer]

	# Replace <br> on new line
	# https://stackoverflow.com/questions/5959415/jquery-javascript-regex-replace-br-with-n
	# regExpStr = r"<br\s*[\/]?>"
	# result = re.sub(regExpStr, os.linesep, chunk)

	result		= chunk
	# result		= general_stuff.removeHtmlTags(chunk)
	result		= result.strip()
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