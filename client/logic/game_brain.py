from client.app.models import *
import numpy as np
from time import sleep
import socketio


class GameBrain:
    """This client-side class manages game states and game data throughout the game.

    It stores data in a format compatible with the database and contains a variety of functions for updating data and managing game states. 
    
    Attributes:
    - game: a "game" object that contains all game settings
    - state: current game state (1: Before game setup)
    - turn: current turn
    - game: a "game" object that contains all game settings
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



    def create_and_push_game(self, name, total_turns, sec_per_turn, starting_money, turns_between_events, player_count,
                             stock_count):

        # CREATE A GAME OBJECT 
        # self.game = Game(*data)
        # Convert game to data
        # data = game.to_dict()
        # self.game = Game(1, name, total_turns, sec_per_turn,  starting_money, turns_between_events, player_count, stock_count, open_=True)
        self.game = Game.create(name, total_turns, sec_per_turn, starting_money, turns_between_events,
                                player_count, stock_count, open_=True)

        # self.game = Game.get_by_id()

        # Game.create(name, total_turns, sec_per_turn, starting_money, turns_between_events, player_count, stock_count)
        # self.game = controller.get_name(name)

        # SEND TO SNOWFLAKE
        # self.game = controller.get_name(name)

    def get_open_games(self):
        # I want a dict: game : [players]
        # Get all games that are open
        # Join with players in game and get players
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

        return dict_game_players

    def join_game(self, gameId, playerId):
        # self.game = Game.get_by_id(gameId)
        # self.player = Player.get_by_id(gameId)
        self.game_id = gameId
        self.player_id = playerId

        # If not connected, connect to the server
        if not self.sio.connected:
            self.sio.connect('http://localhost:5000')
        # Emit the join_game event after connecting
        print("Connecting to the server!!")
        self.sio.emit('join_game', {'player_id': playerId, 'game_id': gameId})

    def leave_game(self, gameId, playerId):
        pass

    def setup_game(self):
        # GET CURRENCY DATA
        N = 20
        curr_1 = 20 * np.random.randn(N) + 400
        curr_2 = 200 * np.random.randn(N) + 300
        curr_3 = 40 * np.random.randn(N) + 300
        curr_4 = 100 * np.random.randn(N) + 1000
        curr_5 = 40 * np.random.randn(N) + 100
        self.currencies = {'USD': curr_1,
                           'JPY': curr_2,
                           'CAD': curr_3,
                           'GBP': curr_4,
                           'BTX': curr_5,
                           }

    def begin_game(self):
        self.state = 2  # DURING TURN
        self.turn = 1

    def next_turn(self):
        N = 20
        if self.turn < 20:
            self.turn += 1
            self.game_state = 3  # BETWEEN TURNS
            print("TURNO!!")

            # UPDATE STOCKS

            # CLOSE TRADES 

            self.game_state = 2
        elif self.turn == 20:
            print('Game ending')
            self.end_game()

    def end_game(self):
        self.game_state = 4  # GAME END

    def send_order(self):
        pass

    def get_sell_orders(self):
        pass

    def get_final_scores(self):
        pass

    def get_portfolio(self):
        pass
