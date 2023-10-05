class Transaction:
    def __init__(self, transaction_id, player_id, game_id, turn_id, stock_id, type_, amount_stock, amount_money, market):
        self.transaction_id = transaction_id
        self.player_id = player_id
        self.game_id = game_id
        self.turn_id = turn_id
        self.stock_id = stock_id
        self.type = type
        self.amount_stock = amount_stock
        self.amount_money = amount_money
        self.market = market

    def create(self):
        # Logic to create a new transaction in the database using Snowflake connection
        pass

    @classmethod
    def get_by_id(cls, transaction_id):
        # Logic to get a transaction by id using Snowflake connection
        pass