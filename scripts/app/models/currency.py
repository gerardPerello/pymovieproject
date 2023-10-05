class Currency:
    def __init__(self, currency_id, name, country, continent):
        self.currency_id = currency_id
        self.name = name
        self.country = country
        self.continent = continent

    def create(self):
        pass

    @classmethod
    def get_by_id(cls, currency_id):
        pass