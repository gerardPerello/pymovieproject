import snowflake.connector 
import os
import sys
sys.path.append('../scripts/credentials')

def connect_snowflake():
    conn = snowflake.connector.connect(
    user=os.getenv('SNOWSQL_USR'), 
    password=os.getenv('SNOWSQL_PWD'), 
    account=os.getenv('SNOWSQL_ACC'),
    warehouse=os.getenv('SNOWSQL_WH'), 
    database=os.getenv('SNOWSQL_DB'),
    schema=os.getenv('SNOWSQL_SCH') ) 
    return conn

def do_operation(operation_name, table_name, data_type, data):
    conn = connect_snowflake()
    
    if(operation_name == "PUSH"):
        push_data(conn, table_name, data_type, data)

    #### ADD MORE
    
    # Close the connection 
    cur.close() 
    conn.close()

def push_data(conn, table_name, data_type, data):
    # Create or use an existing table to hold the JSON 

   
    # Insert the JSON data into the table 
    
    json_str = response.replace("'", "''") #response.text.replace("'", "''") # Escape single quotes 
    cur.execute(f"INSERT INTO {table_name} SELECT PARSE_JSON(COLUMN1) FROM VALUES ('{data}');") 
    


def create_table(conn, table_name, data_query = '(DATA VARIANT)'):
    cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} {data_query};") 
