

DO $$
<<truncate_scheme_tables>>
DECLARE
BEGIN
	
	/*
		Consultations main tables
	*/
	RAISE NOTICE 'Truncate table [raw_consultations] CASCADE!';
	TRUNCATE TABLE raw_consultations CASCADE;
	
	RAISE NOTICE 'Truncate table [consultations] CASCADE!';
	TRUNCATE TABLE consultations CASCADE;
	/*
		/Consultations main tables
	*/
	
	
	
	/*
		Consultation tags
	*/
	RAISE NOTICE 'Truncate table [tags]! CASCADE';
	TRUNCATE TABLE tags CASCADE;
	

	RAISE NOTICE 'Truncate table [consultation_tags]!';
	TRUNCATE TABLE consultation_tags;
	/*
		/Consultation tags
	*/
	
	
	
	/*
		Consultant answers
	*/
	RAISE NOTICE 'Truncate table [answers] CASCADE!';
	TRUNCATE TABLE answers CASCADE;


	RAISE NOTICE 'Truncate table [consultants]! CASCADE';
	TRUNCATE TABLE consultants CASCADE;
	

	RAISE NOTICE 'Truncate table [consultant_answers] CASCADE!';
	TRUNCATE TABLE consultant_answers CASCADE;
	/*
		/Consultant answers
	*/
	
	
	
	/*
		Consultation categories
	*/
	RAISE NOTICE 'Truncate table [categories] CASCADE!';
	TRUNCATE TABLE categories CASCADE;


	RAISE NOTICE 'Truncate table [consultation_categories] CASCADE!';
	TRUNCATE TABLE consultation_categories CASCADE;
	/*
		/Consultation categories
	*/
	
	
	RAISE NOTICE 'Truncate table [questions] CASCADE!';
	TRUNCATE TABLE questions CASCADE;


	RAISE NOTICE 'Truncate table [asking_persons] CASCADE!';
	TRUNCATE TABLE asking_persons CASCADE;
	
	
END truncate_scheme_tables $$;
