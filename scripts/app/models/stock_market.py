class StockMarket:
    def __init__(self, stock_id, game_id, turn_id, stock_value):
        self.stock_id = stock_id
        self.game_id = game_id
        self.turn_id = turn_id
        self.stock_value = stock_value

    def create(self):
        pass

    @classmethod
    def get_by_id(cls, stock_id, game_id, turn_id):
        pass