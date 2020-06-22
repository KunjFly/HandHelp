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


	fileName = "test-1-chunk.html"

	# fileName = "1. doc 1-1000.html"
	# fileName = "2. doc 1001-2000.html"
	# fileName = "3. doc 2001-3000.html"
	# fileName = "4. doc 3001-4000.html"
	# fileName = "5. doc 4001-5000.html"
	# fileName = "6. doc 5001-6000.html"
	# fileName = "7. doc 6001-7000.html"
	# fileName = "8. doc 7001-8000.html"
	# fileName = "9. doc 8001-9000.html"
	# fileName = "10. doc 9001-10000.html"
	# fileName = "11. doc 10001-11000.html"
	# fileName = "12. doc 11001-12000.html"
	fileName = "13. doc 12001-13000.html"
	# fileName = "14. doc 13001-13520.html"
	
	
	
	

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
			"""
			# There is no need to save Success parsed chunks
			"""

			"""
			name           = "SUCCESS_" + parsedChunk["question_number"]
			
			itemToBeWrited = {
				"content"       : parsedChunk
				,"name"         : name
				,"path"         : consts.OUTPUT_FOLDER_LST
				,"timestamp"    : False
			}
			successParsedChunks.append(itemToBeWrited)
			"""

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
		
		
		# if not chunk["raw_text_rest"]:
		# 	"""
		# 	# There is no need to save Success parsed chunks
		# 	"""
		# 	continue
		
		
		# [raw_consultations], [consultations]
		# INSERT INTO raw_consultations
		txt         	= chunk["raw_text"]
		txt_rest    	= chunk["raw_text_rest"]
		is_done     	= 1 if chunk["is_done"] is True else 0
		problem_place	= chunk["problem_place"]
		params		= [
			txt
			,txt_rest
			,is_done
			,problem_place
		]
		query       = f"""
			Insert into raw_consultations (txt, txt_rest, is_done, problem_place)
			values (%s, %s, %s, %s)
			returning id
		"""
		result      = postgres_db.qExec(query, params)
		if not result:
			continue
		id_raw      = result
		logger.info(f"id_raw returning id[{id_raw}]")

		# SELECT FROM consultations
		c_number    = chunk["question_number"]
		params		= [
			c_number
		]
		query       = f"""
			select 1 from consultations
			where c_number = %s
		"""
		result      = postgres_db.qExec(query, params)
		if result is False:
			continue

		# Check if consultation not exists in table
		if len(result):
			id_tag      = result[0][0]
			logger.info(f"c_number exists[{c_number}]! Go to next chunk.")
			continue
		
		# INSERT INTO consultations
		c_date      = chunk["answer_date"]
		params		= [
			id_raw
			,c_number
			,c_date
		]
		query       = f"""
			Insert into consultations (id_raw, c_number, c_date)
			values (%s, %s, %s)
			returning id
		"""
		result      = postgres_db.qExec(query, params)
		if not result:
			continue
		
		id_consultation = result
		logger.info(f"for c_number[{c_number}] id_consultation returning id[{id_raw}]")
		

		# [tags], [consultation_tags]
		# SELECT FROM tags
		tags	= chunk["tags"]
		if tags:
			for tag in tags:
				txt         = tag
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
					logger.info(f"id_tag exists[{id_tag}]")
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
					logger.info(f"id_tag returning id[{id_tag}]")
				
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
				pass
		else:
			logger.info(f"There are no tags for id_consultation[{id_consultation}]")
		
		
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
		logger.info(f"id_answer returning id[{id_answer}]")
		
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
			logger.info(f"id_consultant exists[{id_consultant}]")
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
			logger.info(f"id_consultant returning id[{id_consultant}]")
		
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