from client.app.snowflake_connection import connect_snowflake
import json
import requests
class Player:

    url = "http://127.0.0.1:5000/models/player/"
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def get_all_open(cls):
        new_url = cls.url + 'players/open'
        try:
            response = requests.get(new_url)
            return response.json()
        except Exception as e:
            return {'message': str(e)}

