from client.app.snowflake_connection import connect_snowflake

class ForexHistory:
    def __init__(self, timestamp_id, date, currency_id, value_to_dollar):
        self.timestamp_id = timestamp_id
        self.date = date
        self.currency_id = currency_id
        self.value_to_dollar = value_to_dollar

