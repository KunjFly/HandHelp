DROP DATABASE IF EXISTS handhelp;
CREATE DATABASE handhelp with
	owner				= postgres
	encoding			= 'UTF-8'
	tablespace			= pg_default
	connection limit	= -1
;



DO $$
<<create_scheme_tables>>
DECLARE
BEGIN
	
	/*
		Consultations main tables
	*/
	RAISE NOTICE 'Re-create table [raw_consultations]!';
	
	DROP TABLE IF EXISTS raw_consultations;
	
	CREATE TABLE IF NOT EXISTS raw_consultations (
		id				serial		primary key,
		txt				text		NULL,
		is_done			smallint	NULL,
		processed_date	timestamptz	not null default CURRENT_DATE
	);
	
	
	RAISE NOTICE 'Re-create table [consultations]!';
	
	DROP TABLE IF EXISTS consultations;
	
	CREATE TABLE IF NOT EXISTS consultations (
		id					serial			primary key,
		c_number			integer			not null,	-- Question number
		id_raw				integer			REFERENCES raw_consultations,
		-- id_asking_person	integer			not null,
		-- id_question		integer			not null,
		-- id_answer		integer			not null,
		c_date				timestamptz		null,
		is_outdated			smallint		null
	);
	/*
		/Consultations main tables
	*/
	
	
	
	/*
		Consultation tags
	*/
	RAISE NOTICE 'Re-create table [tags]!';
	
	DROP TABLE IF EXISTS tags;
	
	CREATE TABLE IF NOT EXISTS tags (
		id	serial			primary key,
		txt	VARCHAR(256)	NULL
	);
	
	
	RAISE NOTICE 'Re-create table [consultation_tags]!';
	
	DROP TABLE IF EXISTS consultation_tags;
	
	CREATE TABLE IF NOT EXISTS consultation_tags (
		id				serial		primary key,
		id_consultation	integer		REFERENCES consultations,
		id_tag			integer		REFERENCES tags
	);
	/*
		/Consultation tags
	*/
	
	
	
	/*
		Consultant answers
	*/
	RAISE NOTICE 'Re-create table [answers]!';
	
	DROP TABLE IF EXISTS answers;
	
	CREATE TABLE IF NOT EXISTS answers (
		id	serial		primary key,
		txt	text		null
	);


	RAISE NOTICE 'Re-create table [consultants]!';
	
	DROP TABLE IF EXISTS consultants;
	
	CREATE TABLE IF NOT EXISTS consultants (
		id		serial			primary key,
		name	VARCHAR(256)	NULL
	);
	
	
	RAISE NOTICE 'Re-create table [consultant_answers]!';
	
	DROP TABLE IF EXISTS consultant_answers;
	
	CREATE TABLE IF NOT EXISTS consultant_answers (
		id					serial		primary key,
		id_consultation		integer		REFERENCES consultations,
		id_consultant		integer		REFERENCES consultants,
		id_answer			integer		REFERENCES answers
	);
	/*
		/Consultant answers
	*/
	
	
	
	/*
		Consultation categories
	*/
	RAISE NOTICE 'Re-create table [categories]!';
	
	DROP TABLE IF EXISTS categories;
	
	CREATE TABLE IF NOT EXISTS categories (
		id	serial			primary key,
		txt	VARCHAR(256)	NULL
	);


	DROP TABLE IF EXISTS consultation_categories;
	CREATE TABLE IF NOT EXISTS consultation_categories (
		id					serial		primary key,
		id_consultation		integer		REFERENCES consultations,
		id_category			integer		REFERENCES categories
	);
	/*
		/Consultation categories
	*/
	
	
	DROP TABLE IF EXISTS questions;
	CREATE TABLE IF NOT EXISTS questions (
		id		serial			primary key,
		-- id_c	integer			REFERENCES consultations (id_question),
		id_c	integer			REFERENCES consultations,
		txt		text			NULL
	);


	DROP TABLE IF EXISTS asking_persons;
	CREATE TABLE IF NOT EXISTS asking_persons (
		id		serial			primary key,
		-- id_c	integer			REFERENCES consultations (id_asking_person),
		id_c	integer			REFERENCES consultations,
		name	VARCHAR(256)	NULL
	);
	
	
END create_scheme_tables $$;
