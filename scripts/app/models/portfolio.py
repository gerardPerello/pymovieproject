class Portfolio:
    def __init__(self, player_id, game_id, turn_id, stock_id, amount):
        self.player_id = player_id
        self.game_id = game_id
        self.turn_id = turn_id
        self.stock_id = stock_id
        self.amount = amount

    def create(self):
        pass

    @classmethod
    def get_by_id(cls, player_id, game_id):
        pass