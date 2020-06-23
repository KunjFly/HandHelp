--------------------------------------------------
-- Run script in DBeaver
-- Set scheme handhelp as default before executing
--------------------------------------------------
DO $$
<<create_scheme_tables>>
DECLARE
BEGIN
	
	/*
		Consultations main tables
	*/
	RAISE NOTICE 'Re-create table [raw_consultations]!';
	
	DROP TABLE IF EXISTS raw_consultations CASCADE;
	
	CREATE TABLE IF NOT EXISTS raw_consultations (
		id				serial			primary key,
		txt				text			NULL,
		txt_rest		text			NULL,
		is_done			smallint		NULL,
		problem_place	varchar(265)	NULL,
		processed_date	timestamptz		not null default CURRENT_TIMESTAMP
	);
	
	
	RAISE NOTICE 'Re-create table [consultations]!';
	
	DROP TABLE IF EXISTS consultations CASCADE;
	
	CREATE TABLE IF NOT EXISTS consultations (
		id					serial			primary key,
		c_number			varchar(10)		UNIQUE,							-- Consultation number
		id_raw				integer			REFERENCES raw_consultations ON DELETE CASCADE,
		-- id_asking_person	integer			not null,
		-- id_question		integer			not null,
		-- id_answer		integer			not null,
		c_date				timestamptz		null,
		is_outdated			smallint		null,
		c_note				text			null
	);
	/*
		/Consultations main tables
	*/
	
	
	
	/*
		Consultation tags
	*/
	RAISE NOTICE 'Re-create table [tags]!';
	
	DROP TABLE IF EXISTS tags CASCADE;
	
	CREATE TABLE IF NOT EXISTS tags (
		id	serial			primary key,
		txt	VARCHAR(2048)	UNIQUE
	);
	
	
	RAISE NOTICE 'Re-create table [consultation_tags]!';
	
	DROP TABLE IF EXISTS consultation_tags CASCADE;
	
	CREATE TABLE IF NOT EXISTS consultation_tags (
		id				serial		primary key,
		id_consultation	integer		REFERENCES consultations ON DELETE CASCADE,
		id_tag			integer		REFERENCES tags ON DELETE CASCADE
	);
	/*
		/Consultation tags
	*/
	
	
	
	/*
		Consultant answers
	*/
	RAISE NOTICE 'Re-create table [answers]!';
	
	DROP TABLE IF EXISTS answers CASCADE;
	
	CREATE TABLE IF NOT EXISTS answers (
		id	serial		primary key,
		txt	text		null
	);


	RAISE NOTICE 'Re-create table [consultants]!';
	
	DROP TABLE IF EXISTS consultants CASCADE;
	
	CREATE TABLE IF NOT EXISTS consultants (
		id		serial			primary key,
		name	VARCHAR(2048)	UNIQUE
	);
	
	
	RAISE NOTICE 'Re-create table [consultant_answers]!';
	
	DROP TABLE IF EXISTS consultant_answers CASCADE;
	
	CREATE TABLE IF NOT EXISTS consultant_answers (
		id					serial		primary key,
		id_consultation		integer		REFERENCES consultations ON DELETE CASCADE,
		id_consultant		integer		REFERENCES consultants ON DELETE CASCADE,
		id_answer			integer		REFERENCES answers ON DELETE CASCADE
	);
	/*
		/Consultant answers
	*/
	
	
	
	/*
		Consultation categories
		TODO: fill later when I will parse consultations by categories.
	*/
	RAISE NOTICE 'Re-create table [categories]!';
	
	DROP TABLE IF EXISTS categories CASCADE;
	
	CREATE TABLE IF NOT EXISTS categories (
		id	serial			primary key,
		txt	VARCHAR(2048)	UNIQUE
	);


	DROP TABLE IF EXISTS consultation_categories CASCADE;
	CREATE TABLE IF NOT EXISTS consultation_categories (
		id					serial		primary key,
		id_consultation		integer		REFERENCES consultations ON DELETE CASCADE,
		id_category			integer		REFERENCES categories ON DELETE CASCADE
	);
	/*
		/Consultation categories
	*/
	
	
	DROP TABLE IF EXISTS questions CASCADE;
	CREATE TABLE IF NOT EXISTS questions (
		id				serial			primary key,
		id_consultation	integer			REFERENCES consultations ON DELETE CASCADE,
		txt				text			NULL
	);


	DROP TABLE IF EXISTS asking_persons CASCADE;
	CREATE TABLE IF NOT EXISTS asking_persons (
		id				serial			primary key,
		id_consultation	integer			REFERENCES consultations ON DELETE CASCADE,
		name			VARCHAR(2048)	NULL
	);
	
	
END create_scheme_tables $$;
