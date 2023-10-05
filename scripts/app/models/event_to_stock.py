class Event_to_Stock:
    def __init__(self, event_id, game_id, currency_id):
        self.event_id = event_id
        self.game_id = game_id
        self.currency_id = currency_id

    def create(self):
        pass

    @classmethod
    def get_by_id(cls, event_id, game_id, currency_id):
        pass