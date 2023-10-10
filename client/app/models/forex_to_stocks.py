from client.app.snowflake_connection import connect_snowflake  # Your actual connection setup might be different


class ForexToStock:
    def __init__(self, stock_id, currency_id, currency_weight):
        self.stock_id = stock_id
        self.currency_id = currency_id
        self.currency_weight = currency_weight

