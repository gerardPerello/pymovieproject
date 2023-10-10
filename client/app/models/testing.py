import unittest
from client.app.models import *


class TestDatabaseMethods(unittest.TestCase):

    # === Currency ===
    def test_create_currency(self):
        a = Currency.getCurrenciesInGame()
        print(a)

    def test_stock_values(self):
        b = StockMarket.get_all_for_turn_and_game(10,1)
        print(b)



if __name__ == '__main__':
    unittest.main()