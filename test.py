#region Imports
# import chardet # Dependencies: pip install chardet
import html
import re

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

	chunk		= """
Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. 
<br><font size=-1 face="Arial" color="red">Эта консультация неактуальна, т.к. Верховный Суд занял иную позицию, применив изменения закона к ранее осужденным в наиболее гуманном смысле. Приговоры многих осужденных за наркотики должны быть пересмотрены. Определениями от 14 января 2013 года по <a href="http://hand-help.ru/documents/vs_pavlenko.doc" class="link3"><b>делу Павленко</b></a> и от 22 января 2013 года по <a href="http://hand-help.ru/documents/vs_samarin.doc" class="link3"><b>делу Самарина</b></a>. ВС разрешил неопределенность в толковании закона в пользу ранее осужденных. Их действия должны быть переквалифицированы. Постановление Правительства № 1002 о новых размерах применимо к ранее осужденным в части, улучшающей их положение. См. <a href="http://hand-help.ru/doc6.10.html" class="link3"><b>комментарий</b></a></font>.
Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. 
<br><font size=-1 face="Arial" color="red">Эта консультация неактуальна в части, касающейся применения к ранее осужденным Постановления Правительства № 1002 о новых размерах. Верховный Суд занял иную позицию, применив изменения закона к ранее осужденным в наиболее гуманном смысле. Приговоры многих осужденных за наркотики должны быть пересмотрены. Определениями от 14 января 2013 года по <a href="http://hand-help.ru/documents/vs_pavlenko.doc" class="link3"><b>делу Павленко</b></a> и от 22 января 2013 года по <a href="http://hand-help.ru/documents/vs_samarin.doc" class="link3"><b>делу Самарина</b></a>. ВС разрешил неопределенность в толковании закона в пользу ранее осужденных. Их действия должны быть переквалифицированы. См. <a href="http://hand-help.ru/doc6.10.html" class="link3"><b>комментарий</b></a></font>.
Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. 
<b><font color="Red">ВНИМАНИЕ!</font></b>
<br>После публикации этого ответа Президиум Верховного Суда РФ принял <a href="http://hand-help.ru/documents/vs_post_prezidiuma_26.12.2012.pdf" class="link2"><b>Постановление</b></a> от 26 декабря 2012 года.Осужденные, чьи приговоры вступили в силу до 2013 года, <b><u>не теряют право на их пересмотр</u></b> (вопреки буквальному смыслу закона). 
<br>См. <a href="doc3.html#nov165" class="link3"><b>комментарий</b></b></a><br>
Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. 
<br><b><font color="Red">ВНИМАНИЕ!</font></b>
<br>После публикации этого ответа Президиум Верховного Суда РФ принял <a href="http://hand-help.ru/documents/vs_post_prezidiuma_26.12.2012.pdf" class="link2"><b>Постановление</b></a> от 26 декабря 2012 года.Осужденные, чьи приговоры вступили в силу до 2013 года, <b><u>не теряют право на их пересмотр</u></b> (вопреки буквальному смыслу закона). <br>См. <a href="doc3.html#nov165" class="link3"><b>комментарий</b></b></a><br>.
Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. 	
<br><font color="red"><b>Исправлено 01.10.2011</b></font></font></h2>
Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. 
<br><font color="Red"><b>Исправлено 01.10.2011</b></font></h2>
Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. Текст текст текст. 
	"""

	regExpStr	= r"(<br><font (.*)color=\"red\">|<br><font (.*)color=\"red\"><b>|<br><b><font (.*)color=\"Red\">ВНИМАНИЕ!<\/font><\/b>\n|<b><font (.*)color=\"Red\">ВНИМАНИЕ!<\/font><\/b>\n)(.*)(\n.*)?(<\/b><\/a><\/font>\.|<\/b><\/a><\/font>|<\/b><\/b><\/a><br>\.|<\/b><\/b><\/a><br>|<\/b><\/font><\/h2>|<\/b><\/font><\/font><\/h2>)"
	result		= re.findall(regExpStr, chunk, flags=re.IGNORECASE | re.MULTILINE)
	for item in result:
		print("Matched:")
		print( "".join(item) )
	pass

	
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
	
	# t			= "Txt w/ '"
	# t			= "Txt that ' consists ' some quotes ' "
	# n			= 420
	# query       = f"""
	# 	Insert into test (t, n)
	# 	values ('{t}', {n})
	# """
	# query	= query.replace("'", "''")

	# query       = f"""
	# 	Insert into test (t, n)
	# 	values (%s, %s)
	# """
	# params		= ["Txt w/ '", 420]
	# result  = postgres_db.qExec(query, params)
	
	# logger.info(result)

	
	# query   = "select * from test;"
	# result	= postgres_db.qExec(query)
	# logger.info(result)
	
	""""""


	""" 
	HTML STUFF
	 """

	# s		= "<br><br><b>Отвечает&nbsp;Валентина&nbsp;Максовна&nbsp;Фридман, эксперт-консультант по правовым вопросам Центра содействия реформе уголовного правосудия:</b><br>"
	# result	= html.unescape(s)
	# print(result)

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