class FutureTransaction:
    def __init__(self, transaction_id, player_id, game_id, currency_id, amount, price_per_unit, execution_turn):
        self.transaction_id = transaction_id
        self.player_id = player_id
        self.game_id = game_id
        self.currency_id = currency_id
        self.amount = amount
        self.price_per_unit = price_per_unit
        self.execution_turn = execution_turn

    def create(self):
        pass

    @classmethod
    def get_by_id(cls, transaction_id):
        pass