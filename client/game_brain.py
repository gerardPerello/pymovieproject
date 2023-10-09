from .app.models import *
import numpy as np
from time import sleep

class GameBrain:
    """This client-side class manages game states and game data throughout the game. 

    It stores data in a format compatible with the database and contains a variety of functions for updating data and managing game states. 
    """
    def __init__(self):
        self.game = None    # Game is another object that contains all game settings and identifiers
        self.state = 0      # current game state
        self.turn = 0       # current turn
        self.player = None  # current player
        self.players = {}   # all participating players

        # financial data
        self.stocks = {}  
        self.currencies = {} 

    # def __init__(self):
    #     pass

    def create_and_push_game(self, name, total_turns, starting_money, turns_between_events, player_count, stock_count):

        # CREATE A GAME OBJECT 
        #self.game = Game(*data)
        #Convert game to data
        #data = game.to_dict()
        self.game = Game(1, name, total_turns, 1,  starting_money, turns_between_events, player_count, stock_count)

        Game.create(name, total_turns, 50, starting_money, turns_between_events, player_count, stock_count)
        self.game = Game.get_by_id()

        # SEND TO SNOWFLAKE

    def get_open_games(self):
        # I want a dict: game : [players]
        # Get all games that are open
        # Join with players in game and get players
        pass

    def join_game(self, gameId, playerId):
        # self.game = 
        # self.player =

        # self.players = {}   # all participating players
        # # financial data
        # self.stocks = {}  
        # self.currencies = {} 

        self.state = 1 # WAITING FOR START
        pass


    def setup_game(self):
        # GET CURRENCY DATA
        N = 20
        curr_1 = 20  * np.random.randn(N) + 400
        curr_2 = 200 * np.random.randn(N) + 300
        curr_3 = 40  * np.random.randn(N) + 300
        curr_4 = 100 * np.random.randn(N) + 1000
        curr_5 = 40  * np.random.randn(N) + 100
        self.currencies = {'USD': curr_1,
            'JPY': curr_2,
            'CAD': curr_3,
            'GBP': curr_4,
            'BTX': curr_5,
            }

    def begin_game(self):
        self.state = 2 # DURING TURN
        self.turn = 0

    def next_turn(self):
        N = 20
        if self.turn < 20:
            self.turn += 1
            self.game_state = 3 # BETWEEN TURNS
            # self.compute_next_turn()
            # To game end
        elif self.turn == 20:
            self.end_game()

    def compute_next_turn(self):
        sleep(2)
        self.game_state = 2

    def end_game(self):
        self.game_state = 4 # GAME END

    def push_actual_player(self,data):
        # message = controller.create_player(data)
        pass

    def send_order(self):
        pass

