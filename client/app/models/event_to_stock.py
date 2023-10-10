from client.app.snowflake_connection import connect_snowflake  # Your actual connection setup might be different

class Event_to_Stock:
    def __init__(self, event_id, stock_id, game_id):
        self.event_id = event_id
        self.stock_id = stock_id
        self.game_id = game_id

