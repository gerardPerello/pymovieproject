from client.app.snowflake_connection import connect_snowflake
import requests
import json


class Game:

    url = "http://127.0.0.1:5000/models/game/"

    def __init__(self, id, name, total_turns, sec_per_turn, starting_money,
                 turns_between_events, player_count, stock_count, open_):
        self.id = id
        self.name = name
        self.total_turns = total_turns
        self.sec_per_turn = sec_per_turn
        self.starting_money = starting_money
        self.turns_between_events = turns_between_events
        self.player_count = player_count
        self.stock_count = stock_count
        self.open_ = open_

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'total_turns': self.total_turns,
            'sec_per_turn': self.sec_per_turn,
            'starting_money': self.starting_money,
            'turns_between_events': self.turns_between_events,
            'player_count': self.player_count,
            'stock_count': self.stock_count,
            'open': self.open_

        }

    @classmethod
    def create(cls, name, total_turns, sec_per_turn, starting_money, turns_between_events, player_count, stock_count, open_):

        # PACKAGE AND SEND TO SERVER
        new_url = cls.url + 'game'
        data = cls(
            0, name, total_turns, sec_per_turn,
            starting_money, turns_between_events,
            player_count, stock_count, open_
        )

        dict = data.to_dict()

        headers = {
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(new_url, data=json.dumps(dict), headers=headers)
            return response
        except Exception as e:
            return {'message': str(e)}

    @classmethod
    def get_all(cls):
        new_url = cls.url + 'games'

        try:
            response = requests.get(new_url)
            return response.json()
        except Exception as e:
            return {'message': str(e)}

    def get_by_id(cls, game_id):
        new_url = cls.url + 'game'

        try:
            response = requests.get(new_url)
            return response.json()
        except Exception as e:
            return {'message': str(e)}

    @classmethod
    def get_all_open(cls):
        new_url = cls.url + 'games/open'
        try:
            response = requests.get(new_url)
            return response.json()
        except Exception as e:
            return {'message': str(e)}

