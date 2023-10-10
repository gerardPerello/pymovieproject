from decimal import Decimal

from ..models import *
import random
from flask_socketio import emit
import numpy as np
from datetime import datetime, timedelta
class GameBrain:

    def __init__(self, game, new_turn_callback=None, setupPlayers = False):
        self.game = game
        self.turn = 0
        self.currencies_in_game = set()
        self.forex_history_per_currency_in_game = dict()
        self.stocks_in_game = set()
        self.turn_buy_orders = dict()
        self.turn_sell_orders = dict()
        self.stocks_and_currencies = dict()
        self.random_weights_per_stock = dict()
        self.ready_players = set()
        self.connected_players = set()
        self.players = dict()
        if setupPlayers:
            self.setupPlayers()
        self.new_turn_callback = new_turn_callback
        print("Creating")

    def setupPlayers(self):
        # Create the players.
        for i in range(1, self.game.player_count + 1):
            new_player = Player.get_by_id(i)
            print(new_player)
            if new_player == None:
                message = Player.create(f"Player_{i}")
                print(message)
                new_player = Player(i, f"Player_{i}")

            self.players[i] = new_player
        print(self.players)
        # Create the playersToThisGame
        for player_id in self.players:
            message = PlayersToGame.create(self.game.id, player_id, 1, self.game.starting_money)
            print(message)

    def setupGame(self):

        # Select the N random stocksID's that are going to be in to the game
        allCurrencies = Currency.get_all()
        random.seed(34)
        self.currencies_in_game = random.sample(allCurrencies,self.game.stock_count)
        print(self.currencies_in_game)

        #Select the random values for each turn. We are going to do this selecting an interval from the 100 forexHistory
        num1 = np.random.randint(0, 500-self.game.total_turns)
        num2 = num1 + self.game.total_turns

        base_date = datetime(2011, 1, 1)
        date1 = base_date + timedelta(days=num1)
        date2 = base_date + timedelta(days=num2)



        for c_ in self.currencies_in_game:
            self.forex_history_per_currency_in_game[c_.id] = (
                ForexHistory.get_by_date_range_and_currency(date1, date2, c_.id))


        # Create the stocks
        for currency in self.currencies_in_game:
            print(currency)
            new_stock = Stock.create(currency.code)
            self.stocks_in_game.add(new_stock)
            self.stocks_and_currencies[new_stock.id] = currency.id

            # Select a random for each stock/turn.
        self.random_weights_per_stock = dict()
        for obj in self.stocks_and_currencies.keys():
            self.random_weights_per_stock[obj] = {}  # Create an empty dictionary for each object
            for turn in range(1, self.game.total_turns + 1):
                weight = random.uniform(0, 2)  # Generate a random weight between 0 and 1
                self.random_weights_per_stock[obj][turn] = weight
        print(self.random_weights_per_stock)

        # Create forex to stocks.
        for stock_id in self.stocks_and_currencies:
            print("Creating ForexToStock")
            ForexToStock.create(stock_id, self.stocks_and_currencies[stock_id], 1)

        print(self.forex_history_per_currency_in_game)
        print(self.stocks_and_currencies)
        # NOW WE SHOULD SEND ONLY INFORMATION ABOUT THE STOCKS HERE
        for stock_id in self.stocks_and_currencies:
            print("Creating forex History")
            StockMarket.create(stock_id, self.game.id, 1,
                               self.forex_history_per_currency_in_game[self.stocks_and_currencies[stock_id]][0].value_to_dollar)

        self.start_game()

    def add_order(self, order, type):
        if type == "BUY":
            self.turn_buy_orders[order.id](order)
        else:
            self.turn_sell_orders[order.id](order)

    def cancel_order(self, order_id):
        self.turn_buy_orders.pop(order_id)

    def set_player_ready(self, player_id):
        self.ready_players.add(player_id)
        if self.all_players_ready_to_change_turn():
            self.next_turn()

    def add_connected_player(self, player_id):
        print(player_id)
        self.connected_players.add(player_id)
        emit('player_joined', {'player_id': player_id}, room=self.game.id)
        if self.all_players_ready_to_start():
            self.setupGame()

    def remove_connected_player(self, player_id):
        self.connected_players.discard(player_id)

    def all_players_ready_to_change_turn(self):
        return len(self.ready_players) == len(self.connected_players)

    def all_players_ready_to_start(self):
        return len(self.connected_players) == self.game.player_count

    def start_game(self):
        # Logic to handle turn transition
        print("Starting the GAME")
        self.turn += 1
        if self.new_turn_callback:
            self.new_turn_callback()  # Notify external code that a new turn should start

    def next_turn(self):
        # Logic to handle turn transition
        self.turn += 1

        self.match_orders()  # Set what orders are finally done, update the money of the players.
        self.update_stocks_values()  # Calculate new values for the stocks based on the disponibility and other thinks.

        if self.new_turn_callback:
            self.new_turn_callback()  # Notify external code that a new turn should start
            self.ready_players.clear()  # Restart the players ready.

    def match_orders(self):
        pass

    def update_stocks_values(self):
        print("Creating forex History")
        cont = 1
        for stock_id in self.stocks_and_currencies:

            print(self.turn)
            try:
                StockMarket.create(stock_id, self.game.id, self.turn,
                               self.forex_history_per_currency_in_game[self.stocks_and_currencies[stock_id]][
                                   self.turn-1].value_to_dollar * Decimal(str(self.random_weights_per_stock[stock_id][self.turn])))
            except Exception as e:
                StockMarket.create(stock_id, self.game.id, self.turn,
                                   self.forex_history_per_currency_in_game[self.stocks_and_currencies[stock_id]][
                                       0].value_to_dollar * Decimal(str(self.random_weights_per_stock[stock_id][self.turn])))
            cont+=1
