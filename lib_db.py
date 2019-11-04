#region Imports
import psycopg2 # Dependencies: 1. Install Python (version < 3.8) [actual at 03.11.2019] 2. Install PostgreSQL 3. pip install psycopg2-binary
from psycopg2.extras import DictCursor
from inspect import stack
from contextlib import closing

import lib_config
from lib_io import *
#endregion Imports


#region Functions

def _getConnStr() -> str:
    config = lib_config.getConfigValues()
    connStr = "host='{}' dbname='{}' user='{}' password='{}'".format(
        config["host"]
        ,config["dbname"]
        ,config["user"]
        ,config["password"]
    )
    return connStr


def select(query: str, params: list = []) -> dict:
    funcName = stack()[0][3]

    if query.lower().find("select") == -1:
        errF("{}: query is not select.", funcName)
        return None

    connStr = _getConnStr()
    with closing( psycopg2.connect(connStr) ) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            try:
                cursor.execute(query, params)
                if cursor.rowcount:
                    records = cursor.fetchall()
                    return records
                else:
                    warnF("{}: no data was selected", funcName)
                    return None
            except Exception as ex:
                errF("{}: Exception: [{}].", funcName, ex)
                return None


def insert(query: str, params: list = []) -> int:
    funcName = stack()[0][3]

    if query.lower().find("insert") == -1:
        errF("{}: query is not insert.", funcName)
        return None

    connStr = _getConnStr()
    with closing( psycopg2.connect(connStr) ) as conn:
        conn.autocommit = True
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            try:
                cursor.execute(query, params)
                if query.lower().find("returning id") != -1:
                    id = cursor.fetchone()[0]
                    return id
                else:
                    return None
            except Exception as ex:
                errF("{}: Exception: [{}].", funcName, ex)
                return None
    pass


def truncateTable(tableName):
    funcName = stack()[0][3]

    query = f"TRUNCATE table {tableName}"
    connStr = _getConnStr()
    with closing( psycopg2.connect(connStr) ) as conn:
        conn.autocommit = True
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            try:
                cursor.execute(query)
                return 1
            except Exception as ex:
                errF("{}: Exception: [{}].", funcName, ex)
                return None


def alterSeq(seqName: str, count: int):
    funcName = stack()[0][3]
    
    query = f"ALTER SEQUENCE {seqName} RESTART WITH {count}"
    connStr = _getConnStr()
    with closing( psycopg2.connect(connStr) ) as conn:
        conn.autocommit = True
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            try:
                cursor.execute(query)
                return 1
            except Exception as ex:
                errF("{}: Exception: [{}].", funcName, ex)
                return None

# def update(query: str, params: list = []):
#     pass


# def delete(query: str, params: list = []):
#     pass

#endregion Functions


#region MainCode
def main_db(): # Test

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
    result = select(query, params)

    # Insert (incorrect)
    query = "INSERT INTO users2 (name, age) VALUES (%(Name)s, %(Age)s);"
    result = select(query, params)

    pass

#endregion MainCode


#region Startup
if __name__=="__main__":
    print("Module executed as main")
    main_db()
else:
    print("Module [{0}] imported".format(__name__))
#endregion Startup