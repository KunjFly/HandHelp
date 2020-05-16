--CREATE OR REPLACE FUNCTION print(msg text) 
--  RETURNS integer AS 
--$$ 
--DECLARE 
--BEGIN 
--    RAISE NOTICE USING MESSAGE = msg;
--    RETURN null;
--END; 
--$$ 
--LANGUAGE 'plpgsql' IMMUTABLE;



DO $$
declare

	r record;

begin
	
	perform print('[Script start]');
	
    FOR r in
    	SELECT rc.id
    	FROM raw_consultations rc
		WHERE 1=1
			and rc.is_done = 0
    loop
    
--        EXECUTE 'GRANT ALL ON ' || quote_ident(r.table_schema) || '.' || quote_ident(r.table_name) || ' TO webuser';
--        perform print( CAST (r.id AS text) );
		perform print( CAST (r AS text) );
	
		delete from consultations
		where id_raw = r.id;
	
		delete from raw_consultations
		where id = r.id;

	
    END LOOP;
   	
	perform print('[Script end]');
	
end
$$;


