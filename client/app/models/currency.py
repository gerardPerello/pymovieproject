import requests
import json
class Currency:

    url = "http://127.0.0.1:5000/models/currency/"
    def __init__(self, id, code, name, country, continent):
        self.id = id
        self.code = code
        self.name = name
        self.country = country
        self.continent = continent

    @classmethod
    def getCurrenciesInGame(cls):
        new_url = cls.url + 'currencies'
        try:
            response = requests.get(new_url).json()
            print(response)
            currencies = response['currencies']
            allC = [cls(c[0],c[1],c[2],c[3],c[4]) for c in currencies]
            return allC
        except Exception as e:
            return {'message': str(e)}
