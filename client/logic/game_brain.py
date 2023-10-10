from client.app.models import *
import numpy as np
from time import sleep
import socketio
from ..app.models.CONSTANTS import *

class GameBrain:
    """A class that manages the client-side game logic, state, and socket events.

    The class encapsulates all client-side game functionalities including creating,
    joining games, and reacting to various server-side socket events like player joining,
    and new turn events. Also, it keeps the local game state and data in sync with the server.

    Attributes:
    - open_games_req: A boolean flag to keep track if open games are requested.
    - game: An instance of the game object with all relevant game settings.
    - game_id: A unique identifier for the game.
    - state: An integer representing the current game state.
    - turn: An integer representing the current turn in the game.
    - player: A player object for the current player.
    - player_id: A unique identifier for the player.
    - players: A dictionary to store information of all players participating in the game.
    - open_games: A dictionary to store information about all open games available for joining.
    - game_started: A boolean flag indicating whether the game has started or not.
    - stocks: A dictionary to store information about stocks in the game.
    - currencies: A dictionary to store information about currencies in the game.
    - sio: An instance of the socket.io client to manage real-time communication with the server.
    """

    def __init__(self):
        self.open_games_req = False
        self.game = None  #
        self.game_id = 0
        self.state = 0  # current game state
        self.turn = 0  # current turn
        self.player = None
        self.player_id = 0  # current player
        self.players = {}  # all participating players
        self.open_games = dict()
        self.game_started = False

        # financial data
        self.stocks = {}
        self.currencies = {}

        # initialize socket.io client
        self.sio = socketio.Client()

        # define event handlers for socket.io client
        @self.sio.on('connect')
        def on_connect():
            print("Connected to Server!")

        @self.sio.on('disconnect')
        def on_disconnect():
            print("Disconnected from Server!")

        @self.sio.on('player_joined')
        def on_player_joined(data):
            print(f"Player {data['player_id']} has joined the game")

        @self.sio.on('new_turn')
        def on_new_turn():
            print("New turn:")
            if self.turn == 0:
                print("Game Start:")
                self.begin_game()
            else:
                self.next_turn()

    # Functionality to create a new game with specified settings and push to the server.
    def create_and_push_game(self, name, total_turns, sec_per_turn, starting_money, turns_between_events, player_count,
                             stock_count):

        self.game = Game.create(name, total_turns, sec_per_turn, starting_money, turns_between_events,
                                player_count, stock_count, open_=True)

    # Function to fetch all open games from the server and update the local 'open_games' attribute.
    def get_open_games(self):
        self.open_games_req = True
        dict_game_players = dict()
        try:
            openGames = Game.get_all_open()['games']
            openPlayers = Player.get_all_open()['players']

            dict_game_players = dict()
            for i in openGames:
                temp = []
                for j in openPlayers:
                    if j[2] == i[0]:
                        temp.append(j[0])
                dict_game_players[i[0]] = temp

            print("openGames:", openGames)
            print("openPlayers:", openPlayers)
        except Exception as e:
            print(e)

        self.open_games = dict_game_players

    # Functionality to enable a player to join a specific game identified by gameId and playerId.
    def join_game(self, gameId, playerId):
        self.game_id = gameId
        self.player_id = playerId

        # If not connected, connect to the server
        if not self.sio.connected:
            self.sio.connect(f'http://{ip}:5000')
        # Emit the join_game event after connecting
        print("Connecting to the server!!")
        self.sio.emit('join_game', {'player_id': playerId, 'game_id': gameId})

    # TODO Placeholder for functionality that allows a player to leave a game. Not implemented.
    def leave_game(self, gameId, playerId):
        pass

    # Setup game data, especially relevant for financial data such as stocks and currencies.
    def setup_game(self):
        print(self.game_id, self.turn)
        values = StockMarket.get_all_for_turn_and_game(self.game_id, self.turn)['values']
        print(values)
        self.currencies = {curr[1]: [float(curr[4])] for curr in values}
        print(self.currencies)
        self.game_started = True

    # Logic to handle the initiation of the game, like setting relevant state and turn variables.
    def begin_game(self):
        self.state = 2  # DURING TURN
        self.turn = 1

    # Notifying the server that the player is ready for the next turn/game action.
    def player_ready(self):
        print("Emitting I'm Ready!")
        self.sio.emit('player_ready', {'player_id': self.player_id, 'game_id': self.game_id})

    # Handling the logic and transitions between turns, updating the financial data and game state.
    def next_turn(self):
        N = 20
        if self.turn < 20:
            self.turn += 1
            self.game_state = 3  # BETWEEN TURNS
            print(f"Now is Turn {self.turn}")

            # UPDATE STOCKS
            values = StockMarket.get_all_for_turn_and_game(self.game_id, self.turn)['values']
            print(values)
            for curr in values:
                self.currencies[curr[1]].append(float(curr[4]))

            # CLOSE TRADES
            # TODO

            self.game_state = 2
        elif self.turn == 20:
            print('Game ending')
            self.end_game()

    # TODO Handling the logic that should be processed at the end of the game.
    def end_game(self):
        self.game_state = 4  # GAME END

    # TODO Placeholder for functionality to send an order (buy/sell) to the server. Not implemented.
    def send_order(self):
        pass

    # TODO Placeholder to get the sell orders. Not implemented.
    def get_sell_orders(self):
        pass

    # TODO Placeholder to retrieve final scores at the end of the game. Not implemented.
    def get_final_scores(self):
        pass

    # TODO Placeholder to retrieve final scores at the end of the game. Not implemented.
    def get_portfolio(self):
        pass
