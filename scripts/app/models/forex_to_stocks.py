class ForexToStock:
    def __init__(self, stock_id, currency_id, currency_weight):
        self.stock_id = stock_id
        self.currency_id = currency_id
        self.currency_weight = currency_weight

    def create(self):
        pass

    @classmethod
    def get_by_id(cls, stock_id, currency_id):
        pass