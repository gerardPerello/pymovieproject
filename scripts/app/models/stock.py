class Stock:
    def __init__(self, stock_id, name):
        self.stock_id = stock_id
        self.name = name

    def create(self):
        pass

    @classmethod
    def get_by_id(cls, stock_id):
        pass