--------------------------------------------------
--	Exec it in Quuery tool for DB postgres
--------------------------------------------------

-- 1.
DROP DATABASE IF EXISTS handhelp;

-- 2.
CREATE DATABASE handhelp with
	owner				= postgres
	encoding			= 'UTF-8'
	tablespace			= pg_default
	connection limit	= -1
;