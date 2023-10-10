from client.app.snowflake_connection import connect_snowflake  # Your actual connection setup might be different

class Transaction:
    def __init__(self, transaction_id, player_id, game_id, turn_id, stock_id, type_, amount_stock, amount_money,
                 market):
        self.id = transaction_id
        self.player_id = player_id
        self.game_id = game_id
        self.turn_id = turn_id
        self.stock_id = stock_id
        self.type = type_
        self.amount_stock = amount_stock
        self.amount_money = amount_money
        self.market = market