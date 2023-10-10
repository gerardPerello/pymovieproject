from .app.models import *
import numpy as np
from time import sleep

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
        self.game = None    # 
        self.state = 0      # current game state
        self.turn = 0       # current turn
        self.player = None  # current player
        self.players = {}   # all participating players

        # financial data
        self.stocks = {}  
        self.currencies = {} 

    def create_and_push_game(self, name, total_turns, sec_per_turn, starting_money, turns_between_events, player_count, stock_count):

        # CREATE A GAME OBJECT 

        self.game = Game(1, name, total_turns, sec_per_turn,  starting_money, turns_between_events, player_count, stock_count, open_=True)
        Game.create(name, total_turns, sec_per_turn, starting_money, turns_between_events, player_count, stock_count, open_=True)
        
        # self.game = Game.get_by_id()

        # SEND TO SNOWFLAKE
        # self.game = controller.get_name(name)

    def get_open_games(self):
        # I want a dict: game : [players]
        # Get all games that are open
        # Join with players in game and get players
        pass

    def join_game(self, gameId, playerId):
        # self.game = Game.get_by_id(gameId)
        # self.player = Player.get_by_id(gameId)
        self.state = 1 # WAITING FOR START

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
        if self.turn < N:
            self.turn += 1
            self.game_state = 3 # BETWEEN TURNS            

            # UPDATE STOCKS

            # CLOSE TRADES 
   
        elif self.turn == N:
            print('----------')
            print('Game ending')
            print('----------')
            self.end_game()

    def end_game(self):
        self.game_state = 4 # GAME END

    def send_order(self):
        pass

    def get_sell_orders(self):
        pass

    def get_final_scores(self):
        pass

    def get_portfolio(self):
        pass