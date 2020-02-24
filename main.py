# region Imports
from inspect import stack

import log
import consts
import io_extra
import chunks_processing
import postgres_db
# endregion Imports


# region MainCode
def main():
	""""""
	logger.info("==================================================")
	logger.info("[Start script]")

	""" 
	clear output and read input
	 """
	io_extra.deleteContentOfFolder(consts.OUTPUT_FOLDER_LST)
	# fileName = "test-1-chunk.html"
	fileName = "test-10-chunks.html"
	# fileName = "test-100-chunks.html"
	# fileName = "test-1000-chunks.html"
	# fileName = "doc_1-11499.html"
	# fileName = "doc_11500-13157.html"

	# linesLst = lib.readFileAsLinesLst(fileName, encoding="ascii")
	# linesLst = lib.readFileAsLinesLst(fileName, encoding="latin-1")
	linesLst = io_extra.readFileAsLinesLst(fileName, encoding="Windows-1251")
	
	
	""" 
	Get chunks
	 """
	chunksLst = chunks_processing.linesLstToChunksLst(linesLst)
	if not chunksLst:
		logger.warning("chunksLst is empty!")
		return
	
	logger.info(f"File {fileName} is loaded.")
	
	
	""" 
	Parse chunks
	 """
	parsedChunksLst = []
	for chunk in chunksLst:
		parsedChunk = chunks_processing.parseChunk(chunk)
		if parsedChunk:
			parsedChunksLst.append(parsedChunk)
	
	
	""" 
	Write chunks to files
	 """
	# io_extra.writeObjsToFilesWithTSname(chunksLst, filePath=consts.OUTPUT_FOLDER_LST)
	successParsedChunks = list()
	problemParsedChunks = list()
	for parsedChunk in parsedChunksLst:
		if not parsedChunk["raw_text_rest"]:
			# del parsedChunk["raw_text_rest"]
			name           = "SUCCESS_" + parsedChunk["question_number"]
			
			itemToBeWrited = {
				"content"       : parsedChunk
				,"name"         : name
				,"path"         : consts.OUTPUT_FOLDER_LST
				,"timestamp"    : False
			}
			successParsedChunks.append(itemToBeWrited)
		else:
			name    = "FAIL"
			isTS    = True
			
			if parsedChunk["question_number"]:
				name        = "FAIL_" + parsedChunk["question_number"]
				isTS        = False
			
			itemToBeWrited = {
				"content"       : parsedChunk
				,"name"         : name
				,"path"         : consts.OUTPUT_FOLDER_LST
				,"timestamp"    : isTS
			}
			problemParsedChunks.append(itemToBeWrited)

	io_extra.writeObjsToFiles(successParsedChunks)
	io_extra.writeObjsToFiles(problemParsedChunks)

	
	""" 
	Write chunks to DB
	 """
	for chunk in parsedChunksLst:
		
		# [raw_consultations], [consultations]
		# INSERT INTO raw_consultations
		txt         = chunk["raw_text"]
		txt_rest    = chunk["raw_text_rest"]
		is_done     = 1 if chunk["is_done"] is True else 0
		params		= [
			txt
			,txt_rest
			,is_done
		]
		query       = f"""
			Insert into raw_consultations (txt, txt_rest, is_done)
			values (%s, %s, %s)
			returning id
		"""
		result      = postgres_db.qExec(query, params)
		if not result:
			continue
		id_raw      = result
		logger.info(f"id_raw returning id = {id_raw}")

		# INSERT INTO consultations
		c_number    = chunk["question_number"]
		c_date      = chunk["answer_date"]
		# c_date      = f"to_timestamp('{c_date}', 'dd.mm.yyyy')"
		params		= [
			c_number
			,id_raw
			,c_date
		]
		query       = f"""
			Insert into consultations (c_number, id_raw, c_date)
			values (%s, %s, %s)
			returning id
		"""
		result      = postgres_db.qExec(query, params)
		if not result:
			continue
		
		id_consultation = result
		logger.info(f"id_consultation returning id = {id_raw}")
		

		# [tags], [consultation_tags]
		# TODO: remove brackets and parse tags by "comma"
		# SELECT FROM tags
		txt         = chunk["tags"]
		params		= [
			txt
		]
		query       = f"""
			select id from tags
			where txt = %s
		"""
		result      = postgres_db.qExec(query, params)
		if result is False:
			continue
		
		# Check if tag not exists in table
		if len(result):
			id_tag      = result[0][0]
			logger.info(f"id_tag exists = {id_tag}")
		else:
			# INSERT INTO tags
			params		= [
				txt
			]
			query       = f"""
				Insert into tags (txt)
				values (%s)
				returning id
			"""
			result      = postgres_db.qExec(query, params)
			if not result:
				continue
			
			id_tag      = result
			logger.info(f"id_tag returning id = {id_tag}")
		
		# INSERT INTO consultation_tags
		params		= [
			id_consultation
			,id_tag
		]
		query       = f"""
			Insert into consultation_tags (id_consultation, id_tag)
			values (%s, %s)
		"""
		result      = postgres_db.qExec(query, params)
		if not result:
			continue
		
		
		# [answers], [consultants], [consultant_answers]
		# INSERT INTO answers
		txt    = chunk["answer"]
		params		= [
			txt
		]
		query       = f"""
			Insert into answers (txt)
			values (%s)
			returning id
		"""
		result      = postgres_db.qExec(query, params)
		if not result:
			continue
		
		id_answer   = result
		logger.info(f"id_answer returning id = {id_answer}")
		
		# SELECT FROM consultants
		name    = chunk["who_answers"]
		params		= [
			name
		]
		query       = f"""
			select id from consultants
			where name = %s
		"""
		result      = postgres_db.qExec(query, params)
		if result is False:
			continue
		
		# Check if consultant not exists in table
		if len(result):
			id_consultant      = result[0][0]
			logger.info(f"id_consultant exists = {id_consultant}")
		else:
			# INSERT INTO consultants
			params		= [
				name
			]
			query       = f"""
				Insert into consultants (name)
				values (%s)
				returning id
			"""
			result      = postgres_db.qExec(query, params)
			if not result:
				continue
			
			id_consultant   = result
			logger.info(f"id_consultant returning id = {id_consultant}")
		
		# INSERT INTO consultant_answers
		params		= [
			id_consultation
			,id_consultant
			,id_answer
		]
		query       = f"""
			Insert into consultant_answers (id_consultation, id_consultant, id_answer)
			values (%s, %s, %s)
		"""
		result      = postgres_db.qExec(query, params)
		if not result:
			continue
		
		
		# [questions], [asking_persons]
		# INSERT INTO questions
		txt    = chunk["question"]
		params		= [
			id_consultation
			,txt
		]
		query       = f"""
			Insert into questions (id_consultation, txt)
			values (%s, %s)
		"""
		result      = postgres_db.qExec(query, params)
		if not result:
			continue
		
		# INSERT INTO asking_persons
		name    = chunk["who_asks"]
		params		= [
			id_consultation
			,name
		]
		query       = f"""
			Insert into asking_persons (id_consultation, name)
			values (%s, %s)
		"""
		result      = postgres_db.qExec(query, params)
		if not result:
			continue
		
		
		# TODO: fill [categories], [consultation_categories]
		pass

	logger.info("[End script]")
	logger.info("==================================================")
# endregion MainCode


#region Startup
logger = log.init()
if __name__=="__main__":
	if logger:
		logger.info(f"This module is executing")
		main()
else:
	logger.info(f"This module is imported")
#endregion Startup