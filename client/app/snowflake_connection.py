import snowflake.connector 
import os


def connect_snowflake():
    """Connects to snowflake using credentials stored in credentials/credentials.py.

    Returns:
        snowflake connection: connection to snowflake
    """
    conn = snowflake.connector.connect(
    user=os.getenv('SNOWSQL_USR'), 
    password=os.getenv('SNOWSQL_PWD'), 
    account=os.getenv('SNOWSQL_ACC'),
    warehouse=os.getenv('SNOWSQL_WH'), 
    database=os.getenv('SNOWSQL_DB'),
    schema=os.getenv('SNOWSQL_SCH') ) 


    print("Snowflake connection successfully.")

    return conn

