CREATE TABLE IF NOT EXISTS test (
		id	serial		primary key,
		t	text		NULL,
		n	integer		null
);
select * from test;

--select * from raw_consultations;
--select * from consultations;

--select * from tags;
--select * from consultation_tags;

--select * from answers;
--select * from consultants;
--select * from consultant_answers;

--select * from questions;
--select * from asking_persons;

-- select * from categories;
-- select * from consultation_categories;



select
	consults.c_number			c_number
	,consults.c_date			c_date
	,ask_persons.name			who_asks
	,questions.txt				question
	,consultants.name			consultant
	,answers.txt				answer
	,tags.txt					tag_txt
--	,consults.is_outdated		is_outdated
	,raw_cons.is_done			raw_con_is_done
	,raw_cons.txt				raw_con_txt
	,raw_cons.txt_rest			raw_con_txt_rest
	,raw_cons.processed_date	raw_con_proc_date
from
	consultations		consults
	,raw_consultations	raw_cons
	,consultation_tags	con_tags
	,tags				tags
	,answers			answers
	,consultants		consultants
	,consultant_answers	cons_answers
	,questions			questions
	,asking_persons		ask_persons
where	1 = 1
	and consults.id_raw		= raw_cons.id
	and consults.id			= con_tags.id_consultation
	and tags.id				= con_tags.id_tag
	and answers.id			= cons_answers.id_answer
	and consultants.id		= cons_answers.id_consultant
	and consults.id			= cons_answers.id_consultation
	and consults.id			= questions.id_consultation
	and consults.id			= ask_persons.id_consultation
;