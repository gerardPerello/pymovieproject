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

def do_operation(operation_name, table_name, data_type, data):

    conn = connect_snowflake()
    cur = conn.cursor()

    if(operation_name == "PUSH"):
        push_data(cur, table_name, data_type, data)

    # Close the connection
    cur.close()
    conn.close()

def push_data(cur, table_name, data, data_query= 'SELECT PARSE_JSON(COLUMN1)'):

    # Insert the JSON data into the table

    cur.execute(f"INSERT INTO {table_name} {data_query} FROM VALUES ('{data}');")



def create_table(cur, table_name, data_query = '(DATA VARIANT)'):

    # Create or use an existing table to hold the JSON
    cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} {data_query};")
