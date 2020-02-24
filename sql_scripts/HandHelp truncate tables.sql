--------------------------------------------------
-- Run script in DBeaver
-- Set scheme handhelp as default before executing
--------------------------------------------------
DO $$
<<truncate_scheme_tables>>
DECLARE
BEGIN
	
	/*
		Consultations main tables
	*/
	RAISE NOTICE 'Truncate table [raw_consultations] CASCADE!';
	TRUNCATE TABLE raw_consultations CASCADE;
	ALTER SEQUENCE raw_consultations_id_seq RESTART WITH 1;
	
	RAISE NOTICE 'Truncate table [consultations] CASCADE!';
	TRUNCATE TABLE consultations CASCADE;
	ALTER SEQUENCE consultations_id_seq RESTART WITH 1;
	/*
		/Consultations main tables
	*/
	
	
	
	/*
		Consultation tags
	*/
	RAISE NOTICE 'Truncate table [tags]! CASCADE';
	TRUNCATE TABLE tags CASCADE;
	ALTER SEQUENCE tags_id_seq RESTART WITH 1;
	
	
	RAISE NOTICE 'Truncate table [consultation_tags]!';
	TRUNCATE TABLE consultation_tags;
	ALTER SEQUENCE consultation_tags_id_seq RESTART WITH 1;
	/*
		/Consultation tags
	*/
	
	
	
	/*
		Consultant answers
	*/
	RAISE NOTICE 'Truncate table [answers] CASCADE!';
	TRUNCATE TABLE answers CASCADE;
	ALTER SEQUENCE answers_id_seq RESTART WITH 1;
	
	
	RAISE NOTICE 'Truncate table [consultants]! CASCADE';
	TRUNCATE TABLE consultants CASCADE;
	ALTER SEQUENCE consultants_id_seq RESTART WITH 1;
	
	RAISE NOTICE 'Truncate table [consultant_answers] CASCADE!';
	TRUNCATE TABLE consultant_answers CASCADE;
	ALTER SEQUENCE consultant_answers_id_seq RESTART WITH 1;
	/*
		/Consultant answers
	*/
	
	
	
	/*
		Consultation categories
	*/
	RAISE NOTICE 'Truncate table [categories] CASCADE!';
	TRUNCATE TABLE categories CASCADE;
	ALTER SEQUENCE categories_id_seq RESTART WITH 1;
	
	
	RAISE NOTICE 'Truncate table [consultation_categories] CASCADE!';
	TRUNCATE TABLE consultation_categories CASCADE;
	ALTER SEQUENCE consultation_categories_id_seq RESTART WITH 1;
	/*
		/Consultation categories
	*/
	
	
	RAISE NOTICE 'Truncate table [questions] CASCADE!';
	TRUNCATE TABLE questions CASCADE;
	ALTER SEQUENCE questions_id_seq RESTART WITH 1;
	
	
	RAISE NOTICE 'Truncate table [asking_persons] CASCADE!';
	TRUNCATE TABLE asking_persons CASCADE;
	ALTER SEQUENCE asking_persons_id_seq RESTART WITH 1;
	
	
END truncate_scheme_tables $$;
