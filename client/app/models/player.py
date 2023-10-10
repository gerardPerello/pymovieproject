import json
import requests
from .CONSTANTS import *
class Player:
    """DOCSTRING NEEDED"""
    url = f"http://{ip}:{port}/models/player/"
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

