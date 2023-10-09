from ..sockets import events
from ..models import *
import random


class GameBrain:

    def __init__(self, game, new_turn_callback=None):
        self.game = game
        self.turn = 0
        self.currencies_in_game = set()
        self.stocks_in_game = set()
        self.turn_buy_orders = dict()
        self.turn_sell_orders = dict()
        self.stocks_and_currencies = dict()
        self.random_weights_per_stock = dict()
        self.ready_players = set()
        self.connected_players = set()
        self.new_turn_callback = new_turn_callback
        print("Creating")

    def setupGame(self):
        pass

        # Select the N random stocksID's that are going to be in to the game
        allCurrencies = Currency.get_all()
        self.currencies_in_game = random.sample(allCurrencies, game.stock_count)

        # Select a random for each stock/turn.
        self.random_weights_per_stock = dict()
        for obj in range(1, game.stock_count + 1):
            self.random_weights_per_stock[obj] = {}  # Create an empty dictionary for each object
            for turn in range(1, game.total_turns + 1):
                weight = random.uniform(0, 2)  # Generate a random weight between 0 and 1
                self.random_weights_per_stock[obj][turn] = weight

        # Create the stocks
        for currency in self.currencies_in_game:
            new_stock = Stock.create(currency.code)
            self.stocks_in_game.add(new_stock)
            self.stocks_and_currencies[new_stock.id] = currency.id

        # Create forex to stocks.
        for stock_id in self.stocks_and_currencies:
            ForexToStock.create(stock_id, self.stocks_and_currencies[stock_id], 1)

        # NOW WE SHOULD SEND ONLY INFORMATION ABOUT THE STOCKS HERE

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
        if self.all_players_ready():
            self.next_turn()

    def add_connected_player(self, player_id):
        self.connected_players.add(player_id)

    def remove_connected_player(self, player_id):
        self.connected_players.discard(player_id)

    def all_players_ready(self):
        return len(self.ready_players) == len(self.connected_players)

    def start_game(self):
        # Logic to handle turn transition
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

    def set_state(self, new_state):
        self.state = STATES[new_state]()

    def execute(self):
        self.state.execute(self)

    def match_orders(self):
        pass

    def update_stocks_values(self):
        pass
