CREATE TABLE simple_data
(
    id SERIAL PRIMARY KEY,
    raw_text text,
	question_number text,
	who_asks text,
	tags text,
	question text,
	who_answers text,
	answer text,
	answer_date text,
	raw_text_rest text
);

TRUNCATE table simple_data;
ALTER SEQUENCE simple_data_id_seq RESTART WITH 1;

INSERT INTO simple_data (
	raw_text, question_number, who_asks, tags, question, who_answers, answer, answer_date, raw_text_rest
)
VALUES (
	'raw_text', 'question_number', 'who_asks', 'tags', 'question', 'who_answers', 'answer', 'answer_date', 'raw_text_rest'
);

select * from simple_data;

select count(*) from simple_data;

select * from simple_data
where 1=1
and raw_text_rest is not null;

select count(*) from simple_data
where 1=1
and raw_text_rest is not null;