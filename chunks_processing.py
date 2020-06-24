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
		,"question_edited"	: None
		,"who_answers"      : None
		,"answer"           : None
		,"answer_edited"	: None
		,"answer_date"      : None
		,"raw_text_rest"    : None
		,"problem_place"	: None
		,"note"				: None
		,"previous"			: None
	}


	# Replace HTML entities
	chunk	= html.unescape(chunk)


	# Get [question_number]
	regExpStr	= r"(<a[ ]{0,}name=\".*?\">.*?[№])(.*?)(<\/a>|\/a>)"
	result		= re.findall(regExpStr, chunk, flags=re.IGNORECASE)

	if result and len(result) > 0 and len(result[0][1]) > 0:
		fullResultQnum	= "".join(result[0])
		result			= result[0][1]
		chunk			= chunk.replace(fullResultQnum, "") # remove part [question_number] from chunk

		result			= result.strip()
		parsedChunk["question_number"] = result
	else:
		parsedChunk["raw_text_rest"] = chunk
		parsedChunk["problem_place"] = "1. question_number"
		return parsedChunk
	
	

	# Get [note] (it can be empty)
	regExpStr	= r"(<br><font .*color=\"red\">|<br><font .*color=\"red\"><b>|<br><b><font .*color=\"Red\">ВНИМАНИЕ!<\/font><\/b>\n|<b><font .*color=\"Red\">ВНИМАНИЕ!<\/font><\/b>\n)(.*)(\n.*)?(<\/b><\/a><\/font>\.|<\/b><\/a><\/font>|<\/b><\/b><\/a><br>\.|<\/b><\/b><\/a><br>|<\/b><\/font><\/h2>|<\/b><\/font><\/font><\/h2>)"
	result		= re.findall(regExpStr, chunk, flags=re.IGNORECASE | re.MULTILINE)

	if result and len(result) > 0:
		fullResultNotes	= ""
		for item in result:
			note	= "".join(item)
			chunk	= chunk.replace(note, "") # remove part [note] from chunk

			if fullResultNotes == "":
				fullResultNotes	= note
			else:
				fullResultNotes	+= ";\n" + note
		
		fullResultNotes = fullResultNotes.strip()
		parsedChunk["note"] = fullResultNotes
	


	# Get [previous] consultations (it can be empty)
	regExpStr	= r"(<br>предыдущи(й|е) ?(вопросы?)? ?<a.*?><b>[ ]?№?[ ]?\d{1,5}<\/b><\/a>\n|<br><a.*?><b>предыдущи(й|е) ?<\/b><\/a>[ ]?№?[ ]?\d{1,5}\n|<br>предыдущи(й|е) ?(вопросы?)? ?<a.*?><b>№? ?\d{1,5}<\/b><\/a> ?\n|<br><a.*?><b>предыдущи(й|е) ?(вопросы?)? ?№?\d{1,5}<\/b><\/a>\.?\n|<br>предыдущи(й|е) ?(вопросы?)? ?(<b>)?№? ?\d{1,5}(, \d{1,5})*(<\/b>)?\.?\n|<br>предыдущи(й|е) ?\d{1,5} ?<a.*?>(.*?)</a>\n|<br>(<b>)?(<i>)?\(предыдущи(й|е):? ?№? ?\d{1,5}(.*?)\)(<\/i>)?<\/b>\n|<br><i>\(?предыдущи(й|е) ?\d{1,5} ?<a.*?>.*?<\/a>\)<\/i>\n?|<br><i>\(предыдущи(й|е) ?\d{1,5}\)<\/i>\n|<br><i>предыдущи(й|е) ?<a.*?><b>№? ?\d{1,5}<\/b><\/a><\/i>\n|<br>предыдущи(й|е) ?<a.*?><b>вопросы? ?№? ?\d{1,5}<\/b><\/a>\.?\n|<br>предыдущие ?(вопросы?|консультаци(я|и))? ?(№|№ №|№№)?:? ?.*?\.?\n| предыдущие вопросы <a.*?><\/a>(, <a.*?><\/a>)*\.| (мои)? ?предыдущие ?(вопросы)?№? \d{1,5} ?((,|и) ?(\d{1,5}|<a.*?>.*?<\/a>))*\.)"
	result		= re.findall(regExpStr, chunk, flags=re.IGNORECASE | re.MULTILINE)
	if result and len(result) > 0:
		fullResultPrev			= result[0][0]
		chunk					= chunk.replace(fullResultPrev, "") # remove part [previous] from chunk
		fullResultPrev			= fullResultPrev.strip()
		parsedChunk["previous"] = fullResultPrev



	# Get [who_asks]
	regExpStr	= r"(<b>|<b><p>|<pb>|<br>)(Вопрос |Спрашивают |Спрашивает |Cпрашивает |Спрашиваете |Пишет |Обращается |Спрашиваешь |Пишут |Дополняет |Пишете |Пишет, |Сапрашивает |Спрашивает|Спраивает |Спрашиваю |Спрашиваеь |Спрашиват | Спрашивает |Спращивает |Скрашивает |Спрашиваеьт |Српрашивает |Спрашвиает |Спрашиванет |CСпрашивает |Спрашивае |Спрашивет |Спрашишвает |Спрашвает |Cпрашиваетт |Спрашивали |Спрашшивает )(.*?)(<\/b>|!<\/b>|<br>|\.:<\/b>|\.<\/b>|\.:|\.)"
	result		= re.findall(regExpStr, chunk, flags=re.IGNORECASE)

	if result and len(result) > 0 and len(result[0][2]) > 0:
		fullResultWhoAsks	= "".join(result[0])
		result				= result[0][2]
		chunk				= chunk.replace(fullResultWhoAsks, "") # remove part [who_asks] from chunk

		# remove last semicolon if exists
		regExpStr	= r"[:]$"
		result		= re.sub(regExpStr, "", result)

		result		= result.strip()
		parsedChunk["who_asks"] = result
	else:
		parsedChunk["raw_text_rest"] = chunk
		parsedChunk["problem_place"] = "2. who_asks"
		return parsedChunk


	# Get [tags] (it can be empty)
	# https://stackoverflow.com/questions/11592033/regex-match-text-between-tags
	regExpStr	= r"\n(<br><i>\()(.*)(\)<\/i>)\n"
	result		= re.findall(regExpStr, chunk, flags=re.IGNORECASE | re.MULTILINE)

	if result and len(result) > 0 and len(result[0][1]) > 0:
		fullResultTags	= "".join(result[0])
		result			= result[0][1]
		chunk			= chunk.replace(fullResultTags, "") # remove part [tags] from chunk

		if result and len(result) > 0:
			result	= result.strip()
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
	fullResultWhoAnswers	= ""
	regExpStr				= r"(<p><b>|<b><p>|<p>|<b>|<p><br>|<P><b><a.*>|<br>|<br><\/b>|<br><b>|<<br>b>|<br><b\.|<br><br>БиЮ|<br><br><b>)( )?(Отвечает |Отаечает |Ответ |Ответ:|Пишет |Отвеачет |твечает |Отвечаете |Отвечает |Отвеачает |Отвевает |Отвечает<a.*><b> |Отвечают )(.*?)(:<\/b>|<\/b>|:)"
	result					= re.findall(regExpStr, chunk, flags=re.IGNORECASE)

	if result and len(result) > 0 and len(result[0][3]) is not None:
		fullResultWhoAnswers	= "".join(result[0])
		result					= result[0][3]
		
		# remove last semicolon if exists
		regExpStr	= r"[:]$"
		result		= re.sub(regExpStr, "", result)

		result		= result.strip()
		parsedChunk["who_answers"] = result
	else:
		parsedChunk["raw_text_rest"] = chunk
		parsedChunk["problem_place"] = "3. who_answers"
		return parsedChunk

	
	# Get [question]
	result	= chunk.split(fullResultWhoAnswers)

	if result and len(result) > 0:
		fullResultQuestion	= result[0]
		chunk	= chunk.replace(fullResultQuestion, "") # remove part [question] from chunk
		chunk	= chunk.replace(fullResultWhoAnswers, "") # remove part [who_answers] from chunk

		fullResultQuestion		= fullResultQuestion.strip()
		parsedChunk["question"] = fullResultQuestion

		fullResultQuestionFixed			= general_stuff.removeHtmlTags(fullResultQuestion, r"(<b>|<\/b>)", re.IGNORECASE | re.MULTILINE)
		parsedChunk["question_edited"]	= fullResultQuestionFixed
	else:
		parsedChunk["raw_text_rest"] = chunk
		parsedChunk["problem_place"] = "4. question"
		return parsedChunk


	# Get [answer_date]
	# Get last line with date
	fullResultAnswerDate	= ""
	regExpStr	= r"(<br>|<br>\n|\n</ol>|</ol>\n|</ul>\n|\n)(\d{1,2}[/.-]\d{2}[/.-]\d{2,4})(\n|\.)?(<\/font><\/h2>|<font><\/h2>|<\/font>|<\/h2>|\.|</b></font>)"
	result		= re.findall(regExpStr, chunk, flags=re.IGNORECASE | re.MULTILINE)

	if result and len(result) > 0 and len(result[-1][1]) > 0:
		parsedChunk["answer_date"]	= result[-1][1]
		fullResultAnswerDate		= "".join(result[-1])
		chunk						= chunk.replace(fullResultAnswerDate, "") # remove part [answer_date] from chunk
	else:
		parsedChunk["raw_text_rest"] = chunk
		parsedChunk["problem_place"] = "5. answer_date"
		return parsedChunk


	# Get [answer]
	fullResultAnswer		= chunk
	fullResultAnswer		= fullResultAnswer.strip()
	parsedChunk["answer"]	= fullResultAnswer

	fullResultAnswerFixed			= general_stuff.removeHtmlTags(fullResultAnswer, r"(<b>|<\/b>)", re.IGNORECASE | re.MULTILINE)
	parsedChunk["answer_edited"]	= fullResultAnswerFixed
	

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