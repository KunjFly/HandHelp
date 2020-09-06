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
		,"answers_count"	: 0
	}


	rmHtmlTagsRegExpStr				= r"(^<\/div>(<\/font>)* *\t*(<p>)*(\n|\\n|\r\n|\\r\\n|\n\r|\\n\\r)*(\t|\\t)*(<p>)*-?((\n|\\n|\r\n|\\r\\n|\n\r|\\n\\r)*(\t|\\t)*-?<br>)*|^<br>|^<\/br>|^<font.*?><br>|^<font.*?>(\n|\\n|\r\n|\\r\\n|\n\r|\\n\\r)*(\t|\\t)*<br>|<br>$|<\/br>$|<font.*?>|(<\/p>)*(<\/div>)*(<\/h2>)*$|<\/font>(<\/h2>)*(<p>)*|<\/font>|<b>|<\/b>)"

	# Replace HTML entities
	chunk		= chunk.replace("&nbsp;", " ")


	# Get [question_number]
	regExpStr	= r"((<a.*?name=\".*?\">.*?№ ?)(.*?) ?(<\/a><p>|\/a><p>|<\/a>|\/a>))"
	result		= re.findall(regExpStr, chunk, flags=re.IGNORECASE)

	if result and len(result) > 0 and len(result[0][2]) > 0:
		fullResultQnum	= result[0][0]
		result			= result[0][2]
		result							= result.strip()
		parsedChunk["question_number"]	= result

		# remove part [question_number] and part before it from chunk
		result	= chunk.split(fullResultQnum)
		if result and len(result) > 1:
			chunk	= result[1]
		else:
			parsedChunk["raw_text_rest"] = chunk
			parsedChunk["problem_place"] = "1. question_number"
			return parsedChunk
		

	else:
		parsedChunk["raw_text_rest"] = chunk
		parsedChunk["problem_place"] = "1. question_number"
		return parsedChunk
	
	

	# Get [note] (it can be empty)
	regExpStr	= r"((<br><font .*color=\"red\">|<br><font .*color=\"red\"><b>|<br><b><font .*color=\"Red\">ВНИМАНИЕ!<\/font><\/b>(\n|\\n)|<b><font .*color=\"Red\">ВНИМАНИЕ!<\/font><\/b>(\n|\\n)|<font color=\"red\"><b>)(.*)((\n|\\n).*)?(<\/b><\/a><\/font>\.|<\/b><\/a><\/font>|<\/b><\/b><\/a><br>\.|<\/b><\/b><\/a><br>|<\/b><\/font><\/h2>|<\/b><\/font><\/font><\/h2>|<\/font><a.*?>.*?<\/a>(<p>)?))"
	result		= re.findall(regExpStr, chunk, flags=re.IGNORECASE | re.MULTILINE)

	if result and len(result) > 0:
		fullResultNotes	= ""
		for item in result:
			note	= item[0]
			chunk	= chunk.replace(note, os.linesep) # remove part [note] from chunk

			if fullResultNotes == "":
				fullResultNotes	= note
			else:
				fullResultNotes	+= ";" + os.linesep + note
		
		fullResultNotes = fullResultNotes.strip()
		parsedChunk["note"] = fullResultNotes
	


	# Get [previous] questions numbers and links (it can be empty)
	regExpStr		= r"(<br>пред(ыдущи(й|е))? ?(вопросы?)? ?<a.*?><b> ?(№|вопрос)? ?\d{1,5}<\/b><\/a>\.? *(\n|\\n)|<br><a.*?><b>предыдущи(й|е) ?<\/b><\/a> ?№? ?\d{1,5}(\n|\\n)|<br>предыдущи(й|е) ?(вопросы?)? ?<a.*?><b>№? ?\d{1,5}<\/b><\/a> ?(\n|\\n)|<br><a.*?><b>предыдущи(й|е) ?(вопросы?)? ?№?\d{1,5}<\/b><\/a>(\.(\n|\\n)|\.|(\n|\\n))|<br>предыдущи(й|е) ?(вопросы?)? ?(<b>)?№? ?\d{1,5}(, \d{1,5})*(<\/b>)?\.?(\n|\\n)|<br>предыдущи(й|е) ?\d{1,5} ?<a.*?>(.*?)</a>(\n|\\n)|<br>(<b>)?(<i>)?\(предыдущи(й|е):? ?№? ?\d{1,5}(.*?)\)(<\/i>)?<\/b>(\n|\\n)|<br><i>\(?предыдущи(й|е) ?\d{1,5} ?<a.*?>.*?<\/a>\)<\/i>(\n|\\n)?|<br><i>\(предыдущи(й|е) ?\d{1,5}\)<\/i>(\n|\\n)|<br><i>предыдущи(й|е) ?<a.*?><b>№? ?\d{1,5}<\/b><\/a><\/i>(\n|\\n)|<br>предыдущи(й|е) ?<a.*?><b>вопросы? ?№? ?\d{1,5}<\/b><\/a>\.?(\n|\\n)|<br>предыдущие ?(вопросы?|консультаци(я|и))? ?(№|№ №|№№)?:? ?.*?\.?(\n|\\n)| предыдущие вопросы <a.*?><\/a>(, <a.*?><\/a>)*\.| (мои)? ?предыдущие ?(вопросы)?№? \d{1,5} ?((,|и) ?(\d{1,5}|<a.*?>.*?<\/a>))*\.|<br><a.*?><b>.*?вопрос.*?<\/b><\/a>.*?дополнение.*?(\.(\n|\\n)|(\n|\\n)))"
	result			= re.findall(regExpStr, chunk, flags=re.IGNORECASE | re.MULTILINE)
	fullResultPrev	= ""

	if result and len(result) > 0:
		fullResultPrev			= result[0][0]
		chunk					= chunk.replace(fullResultPrev, os.linesep) # remove part [previous] from chunk
		fullResultPrev			= fullResultPrev.strip()
		parsedChunk["previous"] = fullResultPrev



	# Get [who_asks]
	regExpStr	= r"((<b><p>|<pb>|<br>|<\/br>|<b>|<\/b>) ?(Вопрос|Спрашивают|Спрашивает|Cпрашивает|Спрашиваете|Пишет|Обращается|Спрашиваешь|Пишут|Дополняет|Пишете|Пишет,|Сапрашивает|Спрашивает|Спраивает|Спрашиваю|Спрашиваеь|Спрашиват|Спрашивает|Спращивает|Скрашивает|Спрашиваеьт|Српрашивает|Спрашвиает|Спрашиванет|CСпрашивает|Спрашивае|Спрашивет|Спрашишвает|Спрашвает|Cпрашиваетт|Спрашивали|Спрашшивает|Спаршивает) ?(.*?)(:<\/b><\/p>|:<\/p><\/b>|:<\/b>|<\/b><\/p>|<\/p><\/b>|<\/b>|<b>|<\/p>|<p>)?(\n|\\n))"
	result		= re.findall(regExpStr, chunk, flags=re.IGNORECASE)

	if result and len(result) > 0 and len(result[0][3]) > 0:
		fullResultWhoAsks	= result[0][0]
		who_asks			= result[0][3]
		chunk				= chunk.replace(fullResultWhoAsks, os.linesep) # remove part [who_asks] from chunk

		# Try to find [previous] questions numbers and links in [who_asks] (it can be empty)
		regExpStr	= r"((\(.*?<a.*?>.*?<\/a>((,|…) ?<a.*?>.*?<\/a>)*\)|<a.*?>.*?<\/a>((,|…) ?<a.*?>.*?<\/a>)*)\.?)"
		result		= re.findall(regExpStr, who_asks, flags=re.IGNORECASE)

		if result and len(result) > 0:
			if fullResultPrev == "":
				fullResultPrev	= result[0][0]
			else:
				fullResultPrev	+= ";\n" + result[0][0]
			parsedChunk["previous"] = fullResultPrev

			# replace part [previous] in [who_asks]
			who_asks	= who_asks.replace(result[0][0], "")

		
		# Remove some html tags, strip, remove last semicolon if exists and after strip again
		who_asks				= general_stuff.removeHtmlTags(who_asks, rmHtmlTagsRegExpStr, re.IGNORECASE)
		who_asks				= who_asks.strip()
		regExpStr				= r":$"
		who_asks				= re.sub(regExpStr, "", who_asks)
		who_asks				= who_asks.strip()


		parsedChunk["who_asks"]	= who_asks
	else:
		parsedChunk["raw_text_rest"] = chunk
		parsedChunk["problem_place"] = "2. who_asks"
		return parsedChunk


	# Get [tags] (it can be empty)
	# https://stackoverflow.com/questions/11592033/regex-match-text-between-tags
	regExpStr	= r"(\n|\\n)(<br><i>\()(.*)(\)<\/i>)(\n|\\n)"
	result		= re.findall(regExpStr, chunk, flags=re.IGNORECASE | re.MULTILINE)

	if result and len(result) > 0 and len(result[0][2]) > 0:
		fullResultTags	= "".join(result[0])
		result			= result[0][2]
		chunk			= chunk.replace(fullResultTags, os.linesep) # remove part [tags] from chunk

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


	# Get [answer_date]
	# Get last line with date
	fullResultAnswerDate	= ""
	regExpStr	= r"((<br>|<br>(\n|\\n)|(\n|\\n)</ol>|</ol>(\n|\\n)|</ul>(\n|\\n)|(\n|\\n))(\d{1,2}[/.-]\d{2}[/.-]\d{2,4})((\n|\\n)|\.)?(<\/font><\/h2>|<font><\/h2>|<\/font>|<\/h2>|\.|</b></font>))"
	result		= re.findall(regExpStr, chunk, flags=re.IGNORECASE | re.MULTILINE)

	if result and len(result) > 0 and len(result[-1][7]) > 0:
		parsedChunk["answer_date"]	= result[-1][7]
		fullResultAnswerDate		= result[-1][0]
		chunk						= chunk.replace(fullResultAnswerDate, "") # remove part [answer_date] from chunk
	else:
		parsedChunk["raw_text_rest"] = chunk
		parsedChunk["problem_place"] = "3. answer_date"
		return parsedChunk


	# Get [who_answers] - can be more than one answer
	fullResultWhoAnswersLst	= []
	who_answersLst			= []
	regExpStr				= r"((\n|\\n)? *(<center>)?(<p><b>|<b><p>|<p>|<b>|<p><br>|<p><b><a.*>|<a.*><p><b>|<p><a.*><b>|<p><a.*<b>|<br>|<br><\/b>|<br><b>|<<br>b>|<br><b\.|<br><br>БиЮ|(<br>)*<b>) ?(Отвечает |Отаечает |Ответ |Ответ:|Пишет |Отвеачет |твечает |Отвечаете |Отвечает |Отвеачает |Отвевает |Отвечает<a.*><b> |Отвечают )(<a.*?><b>)?(.*?)(<\/b><\/a>\:?(<\/b>)?| :<\/b>|: <\/b>|:<\/b>| <\/b>|<\/b>| :|:|<a.*?><b>.*?<\/b><\/a>.*?)?(<\/center>)? *(\(ответ изменен\))?((\:|\.) *(<br>)*<\/b>)((\n|\\n)?<br>)?)"
	result					= re.findall(regExpStr, chunk, flags=re.IGNORECASE)
	
	if result and len(result) > 0:

		for item in result:
			fullResultWhoAnswers	= item[0]
			# who_answers				= item[6] + item[7] + item[8] + item[9] + item[10] + item[11]
			who_answers				= "".join(item[6:11])

			# Remove some html tags, strip, remove last semicolon if exists and after strip again
			who_answers		= general_stuff.removeHtmlTags(who_answers, rmHtmlTagsRegExpStr, re.IGNORECASE)
			who_answers		= who_answers.strip()
			regExpStr		= r":$"
			who_answers		= re.sub(regExpStr, "", who_answers)
			who_answers		= who_answers.strip()

			fullResultWhoAnswersLst.append(fullResultWhoAnswers)
			who_answersLst.append(who_answers)

		parsedChunk["who_answers"]	= who_answersLst
	else:
		parsedChunk["raw_text_rest"] = chunk
		parsedChunk["problem_place"] = "4. who_answers"
		return parsedChunk

	
	# Get [question]
	firstWhoAnswers	= fullResultWhoAnswersLst[0]
	result			= chunk.split(firstWhoAnswers)

	if result and len(result) > 0:
		fullResultQuestion	= result[0]
		chunk	= chunk.replace(fullResultQuestion, "") # remove part [question] from chunk
		# chunk	= chunk.replace(firstWhoAnswers, "") # remove part [who_answers] from chunk

		fullResultQuestion				= fullResultQuestion.strip()
		parsedChunk["question"] 		= fullResultQuestion

		fullResultQuestionFixed			= general_stuff.removeHtmlTags(fullResultQuestion, rmHtmlTagsRegExpStr, re.IGNORECASE)
		fullResultQuestionFixed			= fullResultQuestionFixed.strip()
		parsedChunk["question_edited"]	= fullResultQuestionFixed
	else:
		parsedChunk["raw_text_rest"] = chunk
		parsedChunk["problem_place"] = "5. question"
		return parsedChunk


	# Get [answer] - can be more than one answer
	fullResultAnswersLst		= []
	fullResultAnswerFixedLst	= []
	for whoAnswers in reversed(fullResultWhoAnswersLst):
		result	= chunk.split(whoAnswers)

		if result and len(result) > 0:
			fullResultAnswer		= result[-1]
			chunk	= chunk.replace(whoAnswers, "")			# remove part [whoAnswers] from chunk
			chunk	= chunk.replace(fullResultAnswer, "")	# remove part [fullResultAnswer] from chunk

			fullResultAnswer		= fullResultAnswer.strip()
			fullResultAnswersLst.insert(0, fullResultAnswer)

			regExpStr						= r"(^<\/div>(<\/font>)* ?(<p>)*(\n|\\n)*(<p>)*-?((\n|\\n)*-?<br>)*|^<br>|^<\/br>|^<font.*?><br>|^<font.*?>(\n|\\n)<br>|<br>$|<\/br>$|(<\/p>)*(<\/div>)*(<\/h2>)*$|<font.*?>|<\/font><\/h2>|<\/font>|<b>|<\/b>)"
			fullResultAnswerFixed			= general_stuff.removeHtmlTags(fullResultAnswer, rmHtmlTagsRegExpStr, re.IGNORECASE)
			fullResultAnswerFixed			= fullResultAnswerFixed.strip()
			fullResultAnswerFixedLst.insert(0, fullResultAnswerFixed)
		else:
			break
		pass

	
	parsedChunk["answer"]			= fullResultAnswersLst
	parsedChunk["answer_edited"]	= fullResultAnswerFixedLst
	parsedChunk["answers_count"]	= len(fullResultWhoAnswersLst)
	parsedChunk["is_done"]			= True    
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