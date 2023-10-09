import unittest
from client.app.models import *


class TestDatabaseMethods(unittest.TestCase):

    # === Currency ===
    def test_create_currency(self):
        test_data = [{'code':'MINE', 'name': 'MINE', 'country':'SPANIA', 'continent':'EUROPIAN'}]
        response = Currency.create(test_data)
        print(response)
        self.assertEqual(response['message'], 'Currencies created successfully')

    def test_get_currency_by_id(self):
        currency = Currency.get_by_id(170)
        print(currency)
        self.assertEqual(currency.name, 'MINE')

    # === Player ===
    def test_create_player(self):
        test_data = {'name': 'PlayerOne'}
        response = Player.create(test_data)
        print(response['message'])
        self.assertEqual(response['message'], 'Player created successfully')

    def test_get_player_by_id(self):
        player = Player.get_by_id(1)
        self.assertEqual(player.name, 'PlayerOne')

    # === Game ===
    def test_create_game(self):
        test_data = {
            'id': 1,
            'name': 'TestGame',
            'total_turns': 10,
            'sec_per_turn': 60,
            'starting_money': 1000,
            'turns_between_events': 2,
            'player_count': 4,
            'stock_count': 5,
        }  # Add all required fields here
        response = Game.create(test_data)
        self.assertEqual(response['message'], 'Game created successfully')

    def test_get_game_by_id(self):
        game = Game.get_by_id(1)
        self.assertEqual(game.name, 'TestGame')

    # === PlayersToGame ===
    def test_create_players_to_game(self):
        test_data = {'game_id': 1, 'player_id': 1, 'turn_id': 1, 'amount_of_money': 1000}
        response = PlayersToGame.create(test_data)
        self.assertEqual(response['message'], 'Player_To_Game created successfully')

    def test_get_players_to_game_by_id(self):
        players_to_game = PlayersToGame.get_by_id(game_id=1, player_id=1, turn_id=1)
        self.assertEqual(players_to_game.amount_of_money, 1000)

    # === ForexHistory ===
    def test_create_forex_history(self):
        test_data = [
            {'timestamp': 1, 'date': '2023-10-01', 'currency_id': 1, 'value_to_dollar': 1.0}
        ]
        response = ForexHistory.create(test_data)
        self.assertEqual(response['message'], 'Forex_History created successfully')

    def test_get_forex_history_by_id(self):
        forex_history = ForexHistory.get_by_timestamp_and_currency(1, 1)
        self.assertEqual(forex_history.value_to_dollar, 1.0)


if __name__ == '__main__':
    unittest.main()