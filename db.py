#region Imports
import psycopg2 # Dependencies: 1. Install Python (version < 3.8) [actual at 03.11.2019] 2. Install PostgreSQL 3. pip install psycopg2-binary
from psycopg2.extras import DictCursor
from inspect import stack
from contextlib import closing

import log
import config
import io_extra
#endregion Imports


#region Functions
def _getConnStr() -> str:
    """"""
    config = config.getConfigValues()
    connStr = "host='{}' dbname='{}' user='{}' password='{}'".format(
        config["host"]
        ,config["dbname"]
        ,config["user"]
        ,config["password"]
    )
    return connStr


def select(query: str, params: list = []) -> dict:
    """"""
    if query.lower().find("select") == -1:
        # TODO: Add RegExpr to check if it's real SELECT statement
        logger.error(f"{query}: it's not [SELECT]!")
        return None

    connStr = _getConnStr()
    try:
        with closing( psycopg2.connect(connStr) ) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute(query, params)
                    if cursor.rowcount:
                        records = cursor.fetchall()
                        return records
                    else:
                        logger.warning(f"Select return 0 rows, query=[{query}], params=[{params}]")
                        return None
    except Exception as ex:
        logger.error("Exception occurred!", exc_info=True)
        return None


def insert(query: str, params: list = []) -> int:
    """"""
    if query.lower().find("insert") == -1:
        # TODO: Add RegExpr to check if it's real INSERT statement
        logger.error(f"{query}: it's not [INSERT]!")
        return None

    connStr = _getConnStr()
    try:
        with closing( psycopg2.connect(connStr) ) as conn:
            conn.autocommit = True
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute(query, params)
                    if query.lower().find("returning id") != -1:
                        id = cursor.fetchone()[0]
                        return id
                    else:
                        return None
    except Exception as ex:
        logger.error("Exception occurred!", exc_info=True)
        return None


def truncateTable(tableName):
    """"""
    query = f"TRUNCATE table {tableName}"
    connStr = _getConnStr()
    try:
        with closing( psycopg2.connect(connStr) ) as conn:
            conn.autocommit = True
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query)
                return 1
    except Exception as ex:
        logger.error("Exception occurred!", exc_info=True)
        return None


def alterSeq(seqName: str, count: int):
    """"""
    query = f"ALTER SEQUENCE {seqName} RESTART WITH {count}"
    connStr = _getConnStr()
    try:
        with closing( psycopg2.connect(connStr) ) as conn:
            conn.autocommit = True
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute(query)
                    return 1
    except Exception as ex:
        logger.error("Exception occurred!", exc_info=True)
        return None


# def update(query: str, params: list = []):
#     """"""


# def delete(query: str, params: list = []):
#     """"""
#endregion Functions


#region MainCode
def main_db(): # Test
    """"""
    # trunc
    truncateTable("users")
    truncateTable("users2")


    # Select (correct)
    query = "select * from users where Name = %(Name)s"
    params = {
        "Name" : "Alice"
    }
    result = select(query, params)

    # Select (incorrect)
    query = "select * from users2 where Name = %(Name)s"
    params = {
        "Name" : "Name"
    }
    result = select(query, params)


    # Insert (correct)
    query = "INSERT INTO users (name, age) VALUES (%(Name)s, %(Age)s) returning id;"
    params = {
        "Name" : "Zed"
        ,"Age" : 256
    }
    result = select(query, params)

    # Insert (correct)
    query = "INSERT INTO users (name, age) VALUES (%(Name)s, %(Age)s)"
    result = insert(query, params)

    # Insert (incorrect)
    query = "INSERT INTO users2 (name, age) VALUES (%(Name)s, %(Age)s);"
    result = select(query, params)
#endregion MainCode


#region Startup
logger = log.init()
if __name__=="__main__":
    if logger:
        logger.info(f"This module is executing")
        main_db()
else:
    logger.info(f"This module is imported")
#endregion Startup