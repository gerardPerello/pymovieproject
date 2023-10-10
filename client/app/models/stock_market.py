import requests
import json
class StockMarket:
    """DOCSTRING NEEDED"""
    
    url = "http://127.0.0.1:5000/models/currency/"


    def __init__(self, stock_id, game_id, turn_id,stock_name, stock_value):
        self.stock_id = stock_id
        self.stock_name = stock_name
        self.game_id = game_id
        self.turn_id = turn_id
        self.stock_value = stock_value

    @classmethod
    def get_all_for_turn_and_game(cls, game_id, turn_id):
        new_url = cls.url + f'values/{game_id}/{turn_id}'
        try:
            response = requests.get(new_url)
            return response.json()
        except Exception as e:
            return {'message': str(e)}