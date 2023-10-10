import requests

class Portfolio:
    """Placeholder class that might be useful for future development. Main version of class is probably used server-side."""

    url = "http://172.20.10.2:5000/models/portfolio/" 

    def __init__(self, player_id, game_id, turn_id, stock_id, amount):
        self.player_id = player_id
        self.game_id = game_id
        self.stock_id = stock_id
        self.turn_id = turn_id
        self.amount = amount

    @classmethod
    def get(cls, game_id, player_id, turn):
        new_url = cls.url + 'portfolio'
        try:
            response = requests.get(new_url)
            return response.json()
        except Exception as e:
            print({'message': str(e)})
