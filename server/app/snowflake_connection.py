import snowflake.connector 
import os


def connect_snowflake():
    conn = snowflake.connector.connect(
    user=os.getenv('SNOWSQL_USR'), 
    password=os.getenv('SNOWSQL_PWD'), 
    account=os.getenv('SNOWSQL_ACC'),
    warehouse=os.getenv('SNOWSQL_WH'), 
    database=os.getenv('SNOWSQL_DB'),
    schema=os.getenv('SNOWSQL_SCH') ) 


    print("Snowflake connection successfully.")

    return conn

