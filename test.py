#region Imports
# import chardet # Dependencies: pip install chardet
import log
import io_extra
import postgres_db
import general_stuff
from psycopg2 import sql
# import sqlparse
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
	
	""" 
	ENCODING STUFF
	 """
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

	""""""

	""" 
	REG EXPR
	 """

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
	
	""""""

	
	""" 
	LOG STUFF
	 """
	 
	# if not logger:
	#     return
	
	# logger.debug('debug')
	# logger.info('info')
	# logger.warning('warning')
	# logger.error('error')
	# logger.critical('critical')
	 
	""""""
	
	
	""" 
	DB STUFF
	 """

	# alter seq
	# tableName = "simple_data"
	# tableName = "simple_data2"
	# colName = "id"
	# seqName = f"{tableName}_{colName}_seq"
	# result = alterSeq(seqName, 1)

	# truncate
	# postgres_db.truncateTable("users")    
	# postgres_db.truncateTable("users2")


	# # Select (correct)
	# query = "select * from users where Name = %(Name)s"
	# params = {
	#     "Name" : "Alice"
	# }
	# result = postgres_db.select(query, params)

	# # Select (incorrect)
	# query = "select * from users2 where Name = %(Name)s"
	# params = {
	#     "Name" : "Name"
	# }
	# result = postgres_db.select(query, params)


	# # Insert (correct)
	# query = "INSERT INTO users (name, age) VALUES (%(Name)s, %(Age)s) returning id;"
	# params = {
	#     "Name" : "Zed"
	#     ,"Age" : 256
	# }
	# result = postgres_db.select(query, params)

	# # Insert (correct)
	# query = "INSERT INTO users (name, age) VALUES (%(Name)s, %(Age)s)"
	# result = postgres_db.insert(query, params)

	# # Insert (incorrect)
	# query = "INSERT INTO users2 (name, age) VALUES (%(Name)s, %(Age)s);"
	# result = postgres_db.select(query, params)
	

	# postgres_db.truncateTable("simple_data")

	# query = """
	#     INSERT INTO simple_data (
	#         raw_text, question_number, who_asks, tags, question, who_answers, answer, answer_date, raw_text_rest
	#     )
	#     VALUES (
	#         %(raw_text)s, %(question_number)s, %(who_asks)s, %(tags)s, %(question)s, %(who_answers)s, %(answer)s, %(answer_date)s, %(raw_text_rest)s
	#     ) returning id
	# """
	# params = {
	#     "raw_text": "raw_text"
	# 	,"question_number": None
	# 	,"who_asks": None
	# 	,"tags": None
	# 	,"question": None
	# 	,"who_answers": None
	# 	,"answer": None
	# 	,"answer_date": None
	# 	,"raw_text_rest": None
	# }
	# result = postgres_db.insert(query, params)
	# logger.info(result)
	
	# columns = ('varch', 'txt', 'numb')
	# columns = ['varch', 'txt', 'numb']
	# table   = 'test_t'
	
	# columns = sql.SQL(',').join( map(sql.Identifier, columns) )
	# table   = sql.Identifier(table)
	# stmt = sql.SQL('SELECT {} FROM {} LIMIT 5').format(columns, table)
	# stmt = sql.SQL(f'SELECT {columns} FROM {table} LIMIT 5')
	# logger.info(stmt)
	
	# query = sql.SQL('SELECT {} FROM {}').format(
	#     sql.SQL(',').join(map(sql.Identifier, columns)),
	#     sql.Identifier(table)
	# )
	# result  = postgres_db.select(columns, table)
	

	
	query   = "insert into test_t (varch, txt, numb) values('2', '3', 4)"
	result  = postgres_db.qExec(query)
	logger.info(result)
	
	query   = "Select * from test_t"
	result  = postgres_db.qExec(query)
	# logger.info(type(result))
	logger.info(result)
	
	""""""
	
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