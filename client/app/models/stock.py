from client.app.snowflake_connection import connect_snowflake

class Stock:
    def __init__(self, id, name):
        self.id = id
        self.name = name

