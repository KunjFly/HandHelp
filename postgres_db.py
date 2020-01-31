#region Imports
import psycopg2 # Dependencies: 1. Install Python (version < 3.8) [actual at 03.11.2019] 2. Install PostgreSQL 3. pip install psycopg2-binary
from psycopg2.extras import DictCursor
from psycopg2 import sql
from inspect import stack
from contextlib import closing

import log
import config
import io_extra
#endregion Imports


#region Functions
def _getConnStr() -> str:
    """"""
    cfg = config.getConfigValues()
    connStr = "host='{}' dbname='{}' user='{}' password='{}'".format(
        cfg["host"]
        ,cfg["dbname"]
        ,cfg["user"]
        ,cfg["password"]
    )
    return connStr


def qExec(query):
    """"""
    connStr = _getConnStr()
    
    isSelect    = False
    isInsert    = False
    isReturnId  = False
    
    if query.lower().startswith("select"):
        isSelect    = True
    if query.lower().startswith("insert"):
        isInsert    = True
    if query.lower().endswith("isReturnId"):
        isReturnId  = True
    
    try:
        with closing( psycopg2.connect(connStr) ) as conn:
            
            # Autocommit for Insert
            if isInsert:
                conn.autocommit = True
            
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute(query)

                    if isInsert and isReturnId:
                        id = cursor.fetchone()[0]
                        return id
                                        
                    # Select
                    if isSelect and cursor.rowcount:
                        records = cursor.fetchall()
                        return records
                    if isSelect:
                        records = cursor.fetchall()
                        return []
                    
                    return True
    except Exception as ex:
        logger.error("Exception occurred!", exc_info=True)
        return False


#endregion Functions


#region Startup
logger = log.init()
if __name__=="__main__":
    if logger:
        logger.info(f"This module is executing")
else:
    logger.info(f"This module is imported")
#endregion Startup