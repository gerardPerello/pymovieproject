from client.app.snowflake_connection import connect_snowflake  # Your actual connection setup might be different

class StockMarket:
    def __init__(self, stock_id, game_id, turn_id, stock_value):
        self.stock_id = stock_id
        self.game_id = game_id
        self.turn_id = turn_id
        self.stock_value = stock_value

