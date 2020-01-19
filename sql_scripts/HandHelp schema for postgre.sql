/*
	TODO:	Add FOREIGN KEY for every table
*/

DROP DATABASE handhelp;
CREATE DATABASE handhelp with
	owner				= postgres
	encoding			= 'UTF-8'
	tablespace			= pg_default
	-- LC_COLLATE			= collate
	-- ,LC_CTYPE			= ctype
	connection limit	= -1
;


DROP TABLE raw_consultations;
CREATE TABLE IF NOT EXISTS raw_consultations (
	id		serial		primary key,
	txt		text		NULL,
	is_done	smallint	NULL
);


DROP TABLE asking_persons;
CREATE TABLE IF NOT EXISTS asking_persons (
	id		serial			primary key,
	name	VARCHAR(256)	NULL
);


-- CREATE TABLE IF NOT EXISTS questions (
	-- id	serial		primary key,
	-- txt	text		null
-- );


DROP TABLE consultations;
CREATE TABLE IF NOT EXISTS consultations (
	id					serial		primary key,
	id_asking_person	integer		not null,
	-- id_question			integer		not null,
	question			text		NULL,
	id_answer			integer		not null,
	-- id_tag				integer		not null,
	-- id_category			integer		not null,
	-- id_consultation		integer		not null,
	-- id_similar			integer		not null,
	c_number			integer		not null,
	c_date				timestamptz	null,
	is_outdated			smallint	null
);


DROP TABLE consultants;
CREATE TABLE IF NOT EXISTS consultants (
	id		serial			primary key,
	name	VARCHAR(256)	NULL
);


DROP TABLE tags;
CREATE TABLE IF NOT EXISTS tags (
	id	serial			primary key,
	txt	VARCHAR(256)	NULL
);


DROP TABLE consultation_tags;
CREATE TABLE IF NOT EXISTS consultation_tags (
	id				serial		primary key,
	id_consultation	integer		not null,
	id_tag			integer		not null
);


DROP TABLE answers;
CREATE TABLE IF NOT EXISTS answers (
	id	serial		primary key,
	txt	text		null
);


DROP TABLE consultant_answers;
CREATE TABLE IF NOT EXISTS consultant_answers (
	id					serial		primary key,
	id_consultant		integer		not null,
	id_answer			integer		not null,
	id_consultation		integer		not null
);


DROP TABLE categories;
CREATE TABLE IF NOT EXISTS categories (
	id	serial			primary key,
	txt	VARCHAR(256)	NULL
);


DROP TABLE consultation_categories;
CREATE TABLE IF NOT EXISTS consultation_categories (
	id					serial		primary key,
	id_category			integer		not null,
	id_consultation		integer		not null
);


-- CREATE TABLE IF NOT EXISTS similar_consultations (
	-- id						serial		primary key,
	-- id_consultation			integer		not null,
	-- id_similar_consultation	integer		not null
-- );
